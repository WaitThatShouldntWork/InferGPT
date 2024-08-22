from neo4j import GraphDatabase
from data.models import Question, User
import logging
import json

MAX_CONVERSATION_AGE_DAYS = 90

class GraphConnection:

    def __init__(self, uri, user, password, use_bookmark_manager=False):
        """Manages the graph database connection
        
        Bookmark manager is experimental but may be necessary to ensure we can read our writes between
        sessions as the default neo4j is eventually consistent in a cluster whereas we require causal
        consistency - see https://neo4j.com/docs/operations-manual/current/clustering/introduction/#causal-consistency-explained"""
        # set logging
        logging.basicConfig(level=logging.INFO)
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.use_bookmark_manager = use_bookmark_manager
        if use_bookmark_manager:
            self.bookmark_manager = GraphDatabase.bookmark_manager()

    def _session(self):
        """Create a session, optionally with bookmark manager.
        
        Use this function rather than creating sessions directly.
        TODO: Encapsulate to ensure correct usage."""
        return self.driver.session(bookmark_manager=self.bookmark_manager) if self.use_bookmark_manager else self.driver.session()

    def close(self):
        self.driver.close()

    def print_greeting(self, message):
        """Test method - remove when no longer required."""
        with self._session() as session:
            greeting = session.execute_write(self._create_and_return_greeting, message)
            logging.info(greeting)

    # User methods
    def get_or_create_user(self, username):
        with self._session() as session:
            user = session.execute_write(self._get_or_create_user, username)
            logging.info(user)
        return user
    
    @staticmethod
    def _get_or_create_user(tx, name):
        user = tx.run("MATCH (n:User) "
                        "WHERE n.name = $name "
                        "RETURN n "
                        "LIMIT 1", name=name).single()
        if user is None:
            # TODO: Implement create functionality/call 
            user = tx.run("MATCH (n:User) "
                        "WHERE n.name = 'Charlie' "
                        "RETURN n "
                        "LIMIT 1").single()
        return User(user[0]['userId'], user[0]['name'])

    @staticmethod
    def _create_and_return_greeting(tx, message):
        result = tx.run("CREATE (a:Greeting) "
                        "SET a.message = $message "
                        "RETURN a.message + ', from node ' + id(a)", message=message)
        return result.single()[0]
    
    @staticmethod
    def _extract_graph_answers(jsonl_string):
        # Parse JSONL
        lines = jsonl_string.splitlines()
        result = []
        for line in lines:
            data = json.loads(line)
            if 'properties'  in data['v']:                
                qa = Question(data['q']['properties']['questionId'], data['q']['properties']['question'],data['q']['properties']['intent'], None if 'properties' not in data['v'] or 'value' not in data['v']['properties'] else data['v']['properties']['value'])
                result.append(qa)
        return result
    
    @staticmethod
    def _get_conversation_details(tx, conversationId):
        #result = tx.run("MATCH (u:User)-[r]-(c:Conversation {conversationId: $conversationId})-[r2]-(v:Value)-[r3]-(q:Question) RETURN *", conversationId=conversationId)
        result = tx.run("CALL apoc.export.json.query(\"MATCH (u:User)-[r]-(c:Conversation {conversationId: '"+conversationId+"'})-[r2]-(v:Value)-[r3]-(q:Question) RETURN *\", null, {stream: true})").single()
        return result['data']

    def get_conversation_details(self, conversationId):
        with self._session() as session:
            logging.info('Getting conversation info for conversation : ' + conversationId)
            with self._session() as session, session.begin_transaction() as tx:
                return self._extract_graph_answers(self._get_conversation_details(tx, conversationId))
        
    # TODO: Use the goal name (intent) and lookup id instead
    def start_conversation(self, userId, goalId):
        with self._session() as session:
            conversationId = session.execute_write(self._start_conversation, userId, goalId)
            logging.info('Starting conversation: ' + conversationId)
            return conversationId

    # TODO: Add FITS with initial very large weighting for all goal profiles to initialize  (was MAY_FIT unweighted)
    @staticmethod
    def _start_conversation(tx, userId, goalId):
        result = tx.run("""
            MATCH (u:User {userId: $userId})
            MATCH (g:Goal {goalId: $goalId})
            CREATE (u)-[:HAS]->(c:Conversation { conversationId: randomUUID(), when: datetime()})-[:DISCUSSES]->(g)
            WITH c, g
            MATCH (g)-[:DETERMINES]->(p:Profile)
            CREATE (c)-[:EVALUATES]->(:Assessment)-[:FOR]->(p)
            RETURN DISTINCT c.conversationId AS conversationId
            """, {"userId": userId, "goalId": goalId}).single()
        return result['conversationId']

    # TODO: Previous conversations doesn't have much meaning with the revised model
    # this should maybe look at incomplete Assessments instead
    # def get_previous_conversations(self, userId):
    #     with self.driver.session() as session:
    #         oldConversations = session.execute_write(self._get_previous_conversations, userId, MAX_CONVERSATION_AGE_DAYS)
    #         return oldConversations

    # @staticmethod
    # def _get_previous_conversations(tx, userId, max_age_days):
    #     result = tx.run("""
    #         MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation)-[:DISCUSSES]->(g:Goal)
    #         WHERE c.when >= (datetime() - duration({days: $days}))
    #         AND EXISTS((c)-[:IS_ACTIVE]->(:Question))
    #         RETURN c.conversationId AS id, g.name AS name
    #         """, { "userId": userId, "days": max_age_days } )
    #     return list(result)

    @staticmethod
    def _calculate_value(*, question, dependencies, **_):
        if question.calculation == "+":
            # TODO: Use intent, not name
            return { question.name: sum(dependencies.values()) }
        # TODO: Do the calculations! - look at itertools

    @staticmethod
    def _request_value(*, tx, userId, conversationId, question, previousValue, **_):
        result = tx.run(question.query, {userId: userId, conversationId: conversationId})
        newValue = result.single()
        if newValue != previousValue:
            # TODO: Use intent, not name
            return { question.name: result.single() }

    def _switch_type(self, type):
        match type:
            case "Calculate": return self._calculate_value,
            case "Pull": return self._request_value,
            case _: return

    def update_conversation(self, userId, conversationId, intents=None):
        """Stores question responses and returns the next question.
        
        Recursively updates Pull values and Calculate values until either
        there are no more questions or the next Prompt question is found.

        intents is a dictionary of <intent name>: <value>. Sending {} will fetch the next question."""
        if intents is None:
            intents = {}
        with self._session() as session, session.begin_transaction() as tx:
            while True:
                self._store_conversation_values(tx, userId, conversationId, intents)
                record = self._get_next_question(tx, userId, conversationId)
                if record is None:
                    return
                try:
                    func = self._switch_type(record["question"]["type"])
                    if func is None:
                        break
                    intents = func(tx=tx, userId=userId, conversationId=conversationId, question=record["question"], previousValue=record["value"], dependencies=record["dependencies"])
                except Exception as ex:
                    logging.exception("Error updating conversation")
                    print('Error updating conversation: ', ex)
                    break
            return None if record["question"] is None else Question(record["question"]['questionId'], record["question"]['question'])
            # TODO: Return correct data (question) above

    # Adds the new values as latest values for the user and
    # historical values for the conversation
    # Removes the LEADS_TO relationship if present and the value has changed
    # (Re-)evaluates the predicates from the question and adds a LEADS_TO relationship
    # for all valid paths forward
    # TODO: Don't add Calculated values to user latest
    # TODO: Calculate and store Assessment values
    @staticmethod
    def _store_conversation_values(tx, userId, conversationId, intents):
        result = tx.run("""
            UNWIND keys($intents) AS intent
            MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation {conversationId: $conversationId})
            MATCH (q:Question {intent: intent})
            MERGE (u)-[:USES]->(v:Value:Latest)-[:FOR]->(q)
            ON CREATE SET v.value = $intents[intent]
            ON MATCH SET v.value = $intents[intent]
            WITH intent, c, q
            MERGE (c)-[:USES]->(v:Value:Historical)-[:FOR]->(q)
            ON CREATE SET v.value = $intents[intent]
            WITH intent, c, q
            MATCH (c)-[:USES]->(v:Value:Historical)-[:FOR]->(q)
            WHERE v.value <> $intents[intent]
            SET v.value = $intents[intent]
            WITH c, v, q
            MATCH (v)-[:FOR]->(q)-[:HAS_RESPONSE*]->(q2:Question|Knowledge)
            MATCH (c)-[:USES]->(v2:Value)-[:FOR]->(q2)
            WHERE q2.type = "Calculate"
            DETACH DELETE v2
            WITH c, q2
            MATCH (c)-[:USES]->(:Value)-[r:LEADS_TO]->(q2)
            DELETE r
            """, { "userId": userId, "conversationId": conversationId, "intents": intents})
        result.consume()

    @staticmethod
    def _evaluate_path(tx, userId, conversationId):
        tx.run("""
            MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation {conversationId: $conversationId})-[:USES]->(v:Value)-[:FOR]->(q:Question)<-[:USES|LEADS_TO]-(:Goal|Value)
            WHERE NOT ((v)-[:LEADS_TO]->(:Question|Knowledge))
            MATCH (q)-[p:HAS_RESPONSE]->(t:Question|Knowledge)
            WITH DISTINCT t, v, CASE p.comparison
                WHEN 'T' THEN True
                WHEN 'F' THEN False
                WHEN '=' THEN v.value = p.value
                WHEN '<>' THEN v.value <> p.value
                WHEN '>' THEN v.value > p.value
                WHEN '<' THEN v.value < p.value
                WHEN '>=' THEN v.value >= p.value
                WHEN '<=' THEN v.value <= p.value
                WHEN '<<' THEN p.start < v.value AND v.value < p.end
                WHEN '<<=' THEN p.start < v.value AND v.value <= p.end
                WHEN '<=<' THEN p.start <= v.value AND v.value < p.end
                WHEN '<=<=' THEN p.start <= v.value AND v.value <= p.end
            END AS pred
            WHERE pred
            CREATE (v)-[:LEADS_TO]->(t)
            """, { "userId": userId, "conversationId": conversationId})

    @staticmethod
    def _get_next_question(tx, userId, conversationId):
        # TODO: The sub-query union could be removed if a common relationship type is used (rather than LEADS_TO / USES)
        # TODO: Add Assessment into the main match to exclude Assessment values below some cut-off. Also need to calculate
        # and update Assessment values as part of storing conversation values.
        result = tx.run("""
            MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation {conversationId: $conversationId})-[*]->(p:Profile)
            CALL {
                WITH u, c, p
                MATCH (p)-[:REQUIRES]->(k:Knowledge)<-[:HAS_RESPONSE*]-(q:Question)<-[:LEADS_TO]-(:Value)<-[:USES]-(c)
                WHERE not ((c)-[:USES]->(:Value)-[:FOR]->(q))
                RETURN q, COUNT(k) AS decides
                ORDER BY decides DESC
                LIMIT 1
            UNION
                WITH u, c, p
                MATCH (p)-[:REQUIRES]->(k:Knowledge)<-[:HAS_RESPONSE*]-(q:Question)<-[:USES]-(:Goal)<-[:DISCUSSES]-(c)
                WHERE not ((c)-[:USES]->(:Value)-[:FOR]->(q))
                RETURN q, COUNT(k) AS decides
                ORDER BY decides DESC
                LIMIT 1
            }
            WITH c, q, decides
            ORDER BY decides DESC
            LIMIT 1
            OPTIONAL MATCH (u:User {userId: $userId})-[:USES]->(v:Value)-[:FOR]->(q)
            OPTIONAL MATCH (q)-[:DEPENDS_ON]->(q2)<-[:FOR]-(v2:Value)-[:USES]-(c)
            RETURN q AS question, v.value AS value, apoc.map.fromLists(collect(q2.name), collect(v2.value)) AS dependencies
            """, { "userId": userId, "conversationId": conversationId})
        return result.single()

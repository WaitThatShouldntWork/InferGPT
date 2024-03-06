// NOTE: Copy each line into the Neo4j browser and execute before copying and executing the next line

// TODO: Check preventing duplicate relationships
// TODO: Add conversation id tags to relationships - required? or just timestamp and staleness?
// TODO: Check self-referential ASKS in node graph
// TODO: Add timestamps for stale data

:param userId => 3;
:param goalId => 2;
:param conversationId => 1;

// TODO: Add FITS with initial very large weighting for all goal profiles to initialize  (was MAY_FIT unweighted)
MATCH (u:User {userId: $userId})
MATCH (g:Goal {goalId: $goalId})
CREATE (u)-[:HAS]->(c:Conversation { conversationId: randomUUID(), when: datetime()})-[:ABOUT]->(g)
WITH u, g
MATCH (g)-[:DETERMINES]->(p:Profile)
MERGE (u)-[:FITS]->(a:Assessment {assessmentId: randomUUID()})
WITH DISTINCT c, g
MATCH (g)-[:USES]->(q:Question)
CREATE (c)-[:IS_ACTIVE]->(q)
RETURN DISTINCT c.conversationId;

// Pushed values are automatically used for a conversation
MATCH (:Push)-[:FOR]-(v:Value)-[:PROVIDES]-(u:User {userId: $userId})-[:HAS]-(c:Conversation {conversationId: $conversationId})
CREATE (c)-[:USES]->(v);
// Pulled values are updated if stale
MATCH (:Pull)-[:FOR]-(v:Value)-[:PROVIDES]-(u:User {userId: $userId})-[:HAS]-(c:Conversation {conversationId: $conversationId})
WHERE v.when >= (datetime() - duration({minutes: 10}))
// Pull new value, create new node if not exists else link to existing
CREATE (c)-[:USES]->(v);
// Prompted values need re-confirming
// Calculated values need re-calculating and merge/link accordingly


// TODO: Parameterize max. conversation age
// Find previous incomplete conversations
MATCH (u:User {userId: $userId})-[:FITS]->(a:Assessment {incomplete: True})-[:FOR]-(:Profile)-[:DETERMINES]-(:Goal)-[:ABOUT]-(c:Conversation)
WHERE c.when >= (datetime() - duration({days: 90}))
AND NOT ((c)-[:LINKED_TO]->(:Conversation))
RETURN c.conversationId, g.name;

// Get next question
MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation {conversationId: $conversationId})-[:MAY_FIT]->(p:Profile)
MATCH (p)-[:REQUIRES]->(k:Knowledge)<-[*]-(q:Question)<-[:IS_ACTIVE]-(c)
// WHERE not ((u)-[:HAS_VALUE]->(q))
WITH q, COUNT(k) AS decides
ORDER BY decides DESC LIMIT 1
RETURN q;

// Add HAS_VALUE for all intents for given conversation
UNWIND keys($intents) AS intent
MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation {conversationId: $conversationId})
MATCH (q:Question {intent: intent})
MERGE (c)-[:HAS_VALUE {value: $intents[intent]}]->(q);

MATCH (u:User {userId: $userId})-[:HAS]->(c:Conversation {conversationId: $conversationId})
// TODO: Should probably use a full statement in predicate for more flexibility and less risk
// Evaluate predicates and move IS_ACTIVE to next node
MATCH (u:User {userId: $userId})-[h:HAS_VALUE {conversationId: $conversationId}]->(q:Question)<-[a:IS_ACTIVE {conversationId: $conversationId}]-(u)
MATCH (q)-[r:HAS_RESPONSE]-(nq:Question|:Knowledge)
WHERE CALL apoc.cypher.run("MATCH " + h.value + " " + r.predicate + " AS predicate RETURN predicate", {}) YIELD value
MATCH (nq)
WHERE value.predicate = 1
// Can't ignore as may have to skip over so need to loop
// AND not((u)-[:HAS_VALUE {conversationId: $conversationId}]->(nq))
CREATE (u)-[:IS_ACTIVE {conversationId: $conversationId}]->(nq)
MATCH (u)
DELETE a;

// Export database as cypher statements to replay in Neo4j browser
CALL apoc.export.cypher.all(null, {format: "plain", stream: true}) YIELD cypherStatements RETURN cypherStatements


MATCH (n) DETACH DELETE n

:params {
    "userId": 3,
    "conversationId": "2b4b2e63-8567-4723-a171-4032af5627ac",
    "goalId": 1,
    "intents": {
      "other savings": 6000
    }
}

:params {
    "userId": 3,
    "conversationId": 2,
    "goalId": 1,
    "intents": {
      "other savings": 6000
    }
}

CREATE
(u:User {name: "User", userId: 3}),
(conv:Conversation {conversationId: 2}),
(g:Goal {goalId: 1, name: "investments"}),
(g2:Goal {goalId: 2, name: "financial health"}),
(a:Value:Latest {value: 2000}),
(b:Value:Latest {value: 3000}),
(c:Value:Latest {value: 5000}),
(d:Value:Latest {value: 5000}),
(a2:Value:Historical {value: 2000}),
(b2:Value:Historical {value: 3000}),
(c2:Value:Historical {value: 5000}),
(d2:Value:Historical {value: 5000}),
(q:Question {name: "savings account", intent: "other savings", type: "Push"}),
(q2:Question {name: "other savings", type: "Prompt"}),
(q3:Question {name: "total savings", type: "Calculate"}),
(k:Knowledge {name: "savings >= 5000", type: "Calculate"}),
(k2:Knowledge {name: "savings < 5000", type: "Calculate"}),
(p:Profile {name: "high savings"}),
(p2:Profile {name: "low savings"}),
(g)-[:USES]->(q),
(a)-[:FOR]->(q),
(a)-[:LEADS_TO]->(q2),
(b)-[:FOR]->(q2),
(b)-[:LEADS_TO]->(q3),
(c)-[:FOR]->(q3),
(c)-[:LEADS_TO]->(k),
(d)-[:FOR]->(k),
(a2)-[:FOR]->(q),
(a2)-[:LEADS_TO]->(q2),
(b2)-[:FOR]->(q2),
(b2)-[:LEADS_TO]->(q3),
(c2)-[:FOR]->(q3),
(c2)-[:LEADS_TO]->(k),
(d2)-[:FOR]->(k),
(q)-[:HAS_RESPONSE {comparison: ">=", value: 5000}]->(q3),
(q)-[:HAS_RESPONSE {comparison: "<", value: 5000}]->(q2),
(q2)-[:HAS_RESPONSE {comparison: "T"}]->(q3),
(q3)-[:HAS_RESPONSE {comparison: ">=", value: 5000}]->(k),
(q3)-[:HAS_RESPONSE {comparison: "<", value: 5000}]->(k2),
(q3)-[:DEPENDS_ON]->(q),
(q3)-[:DEPENDS_ON]->(q2),
(k)-[:DEPENDS_ON]->(q),
(k)-[:DEPENDS_ON]->(q2),
(k2)-[:DEPENDS_ON]->(q),
(k2)-[:DEPENDS_ON]->(q2),
(k)<-[:REQUIRES]-(p),
(k2)<-[:REQUIRES]-(p2),
(u)-[:USES]->(a),
(u)-[:USES]->(b),
(u)-[:USES]->(c),
(u)-[:USES]->(d),
(u)-[:HAS]->(conv),
(u)-[:DISCUSSES]->(g),
(conv)-[:DISCUSSES]->(g),
(conv)-[:USES]->(a2),
(conv)-[:USES]->(b2),
(conv)-[:USES]->(c2),
(conv)-[:USES]->(d2),
(g)-[:DETERMINES]->(p),
(g)-[:DETERMINES]->(p2)

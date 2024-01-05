:use neo4j

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/users.csv" AS row
WITH row WHERE row.userId IS NOT NULL
MERGE (:User {userId: toInteger(row.userId), name: row.name});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/goals.csv" AS row
WITH row WHERE row.goalId IS NOT NULL
MERGE (:Goal {goalId: toInteger(row.goalId), name: row.name});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/profiles.csv" AS row
WITH row WHERE row.profileId IS NOT NULL
MERGE (:Profile {profileId: toInteger(row.profileId), name: row.name});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/goals_profiles.csv" AS row
WITH row WHERE row.goalId IS NOT NULL AND row.profileId IS NOT NULL
MATCH (g:Goal {goalId: toInteger(row.goalId)})
MATCH (p:Profile {profileId: toInteger(row.profileId)})
MERGE (g)-[:DETERMINES]->(p);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/usecase_knowledge.csv" AS row
WITH row WHERE row.knowledgeId IS NOT NULL
MERGE (:Knowledge {knowledgeId: toInteger(row.knowledgeId), name: row.name});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/usecase_profiles_knowledge.csv" AS row
WITH row WHERE row.profileId IS NOT NULL AND row.knowledgeId IS NOT NULL
MATCH (p:Profile {profileId: toInteger(row.profileId)})
MATCH (k:Knowledge {knowledgeId: toInteger(row.knowledgeId)})
MERGE (p)-[:REQUIRES {weight: row.weight}]->(k);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/usecase_questions.csv" AS row
WITH row WHERE row.questionId IS NOT NULL
MERGE (q:Question {questionId: toInteger(row.questionId), name: row.name, type: row.type})
FOREACH(ignoreMe IN CASE WHEN row.type = "Prompt" THEN [1] ELSE [] END | SET q.intent = row.intent, q.question = row.question)
FOREACH(ignoreMe IN CASE WHEN row.type = "Pull" THEN [1] ELSE [] END | SET q.query = row.query);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/usecase_questions_knowledge.csv" AS row
WITH row WHERE row.questionId IS NOT NULL AND row.knowledgeId IS NOT NULL
MATCH (q:Question {questionId: toInteger(row.questionId)})
MATCH (k:Knowledge {knowledgeId: toInteger(row.knowledgeId)})
MERGE (q)-[:HAS_RESPONSE {predicate: row.predicate, weight: row.weight}]->(k);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/questions_questions.csv" AS row
WITH row WHERE row.questionId IS NOT NULL AND row.knowledgeId IS NOT NULL
MATCH (q:Question {questionId: toInteger(row.questionId)})
MATCH (q2:Question {questionId: toInteger(row.questionId2)})
MERGE (q)-[:HAS_RESPONSE {predicate: row.predicate, weight: row.weight}]->(q2);

MATCH (g:Goal)-[:DETERMINES]->(:Profile)-[:REQUIRES]->(:Knowledge)<-[:HAS_RESPONSE*]-(q:Question)
MERGE (g)-[:USES]->(q);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/conversations.csv" AS row
WITH row WHERE row.conversationId IS NOT NULL
MERGE (:Conversation {conversationId: toInteger(row.conversationId)});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/conversation_conversation.csv" AS row
WITH row WHERE row.conversationId IS NOT NULL AND row.conversationId2 IS NOT NULL
MATCH (c:Conversation {conversationId: toInteger(row.conversationId)})
MATCH (c2:Conversation {conversationId: toInteger(row.conversationId2)})
MERGE (c)-[:LINKED_TO]->(c2);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/conversation_goal.csv" AS row
WITH row WHERE row.conversationId IS NOT NULL AND row.goalId IS NOT NULL
MATCH (c:Conversation {conversationId: toInteger(row.conversationId)})
MATCH (g:Goal {goalId: toInteger(row.goalId)})
MERGE (c)-[:DISCUSSES]->(g);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/user_conversation.csv" AS row
WITH row WHERE row.userId IS NOT NULL AND row.conversationId IS NOT NULL
MATCH (u:User {userId: toInteger(row.userId)})
MATCH (c:Conversation {conversationId: toInteger(row.conversationId)})
MERGE (u)-[:HAS]->(c);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/assessments.csv" AS row
WITH row WHERE row.assessmentId IS NOT NULL
MERGE (:Assessment {assessmentId: toInteger(row.assessmentId), total: toFloat(row.total), weightedTotal: toFloat(row.weightedTotal)});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/assessment_profile.csv" AS row
WITH row WHERE row.assessmentId IS NOT NULL AND row.profileId IS NOT NULL
MATCH (a:Assessment {assessmentId: toInteger(row.assessmentId)})
MATCH (p:Profile {profileId: toInteger(row.profileId)})
MERGE (a)-[:FOR]->(p);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/conversation_assessment.csv" AS row
WITH row WHERE row.conversationId IS NOT NULL AND row.assessmentId IS NOT NULL
MATCH (c:Conversation {conversationId: toInteger(row.conversationId)})
MATCH (a:Assessment {assessmentId: toInteger(row.assessmentId)})
MERGE (c)-[:EVALUATES]->(a);

// This isn't used and may need removing as it needs recalculating each time a user value updates
// which includes any time a new value is Pushed. This may be acceptable if profiles are used
// pro-actively to trigger backend actions but if only used reactively during a conversation, then
// it either requires unnecessary work or it means that any assessment linked to a user directly
// may be stale and needs checking/recalculating.
// LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/user_assessment.csv" AS row
// WITH row WHERE row.userId IS NOT NULL AND row.assessmentId IS NOT NULL
// MATCH (u:User {userId: toInteger(row.userId)})
// MATCH (a:Assessment {assessmentId: toInteger(row.assessmentId)})
// MERGE (u)-[:FITS]->(a);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/values.csv" AS row
WITH row WHERE row.valueId IS NOT NULL
MERGE (:Value {valueId: toInteger(row.valueId), value: row.value});

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/conversation_value.csv" AS row
WITH row WHERE row.conversationId IS NOT NULL AND row.valueId IS NOT NULL
MATCH (c:Conversation {conversationId: toInteger(row.conversationId)})
MATCH (v:Value {valueId: toInteger(row.valueId)})
MERGE (c)-[:USES]->(v);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/value_knowledge.csv" AS row
WITH row WHERE row.valueId IS NOT NULL AND row.knowledgeId IS NOT NULL AND row.relationshipType = "FOR"
MATCH (v:Value {valueId: toInteger(row.valueId)})
MATCH (k:Knowledge {knowledgeId: toInteger(row.knowledgeId)})
MERGE (v)-[:FOR]->(k);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/value_knowledge.csv" AS row
WITH row WHERE row.valueId IS NOT NULL AND row.knowledgeId IS NOT NULL AND row.relationshipType = "LEADS_TO"
MATCH (v:Value {valueId: toInteger(row.valueId)})
MATCH (k:Knowledge {knowledgeId: toInteger(row.knowledgeId)})
MERGE (v)-[:LEADS_TO]->(k);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/value_question.csv" AS row
WITH row WHERE row.valueId IS NOT NULL AND row.questionId IS NOT NULL AND row.relationshipType = "FOR"
MATCH (v:Value {valueId: toInteger(row.valueId)})
MATCH (q:Question {questionId: toInteger(row.questionId)})
MERGE (v)-[:FOR]->(q);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/value_question.csv" AS row
WITH row WHERE row.valueId IS NOT NULL AND row.questionId IS NOT NULL AND row.relationshipType = "LEADS_TO"
MATCH (v:Value {valueId: toInteger(row.valueId)})
MATCH (q:Question {questionId: toInteger(row.questionId)})
MERGE (v)-[:LEADS_TO]->(q);

LOAD CSV WITH HEADERS FROM "http://localhost:5500/samples/graphdb/user_value.csv" AS row
WITH row WHERE row.userId IS NOT NULL AND row.valueId IS NOT NULL
MATCH (u:User {userId: toInteger(row.userId)})
MATCH (v:Value {valueId: toInteger(row.valueId)})
MERGE (u)-[:USES]->(v);

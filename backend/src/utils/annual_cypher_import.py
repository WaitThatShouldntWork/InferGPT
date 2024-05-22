annual_transactions_cypher_script = """
WITH $data AS data
UNWIND data.all_data[0..1] as info

FOREACH (_ IN CASE WHEN info.account.display_name IS NOT NULL THEN [1] ELSE [] END |
    MERGE (a:Account {name:info.account.display_name})
    FOREACH (transactions IN info.transactions |
        FOREACH (t IN transactions |
            MERGE (transaction:Transaction {id: t.transaction_id})
            ON CREATE SET
                transaction.amount = t.amount,
                transaction.description = t.description,
                transaction.date = datetime(t.timestamp),
                transaction.type = t.transaction_type
            MERGE (transaction)-[:PAID_BY]->(a)

            FOREACH (_ IN CASE WHEN t.merchant_name IS NOT NULL THEN [1] ELSE [] END |
                MERGE (merchant:Merchant {name: t.merchant_name})
                MERGE (transaction)-[:PAID_TO]->(merchant)
            )

            FOREACH (_ IN CASE WHEN size(t.transaction_classification) = 0 THEN [1] ELSE [] END |
                MERGE (uncategorized:Classification {name: "Uncategorized"})
                MERGE (transaction)-[:CLASSIFIED_AS]->(uncategorized)
            )

            FOREACH (payment_classification IN t.transaction_classification |
                MERGE (classification:Classification {name:payment_classification})
                MERGE (transaction)-[:CLASSIFIED_AS]->(classification)
            )
        )
    )
)
"""

remove_credits = """
MATCH (n:Transaction {type: "CREDIT"})
DETACH DELETE n
"""

remove_transactions_without_merchant = """
MATCH (n:Transaction)-[r:PAID_TO]->(a:Merchant)
WHERE a IS NULL
DETACH DELETE n
"""

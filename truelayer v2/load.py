import os
import random
from configparser import ConfigParser

from neo4j import GraphDatabase


class Load:
    def __init__(self):
        env = os.getenv("ENV", ".config")

        if env == ".config":
            config = ConfigParser()
            config.read(".config")
            config = config["NEO4J"]

        self.uri = config['NEO4J_URI']
        self.user = config['NEO4j_USERNAME']
        self.password = config['NEO4j_PASSWORD']
        self.database = config['NEO4J_DB']

        self.my_node = 'MERGE (c:Customer {id: 1, firstName: "Michael", middleName: "Keevil", lastName: "Down", dob: date("1988-02-02")})'

        # neo4j connection
        self.driver = GraphDatabase.driver(f"{self.uri}/db/{self.database}", auth=(self.user, self.password))

    def write_accounts(self, account):
        # anonymise account details
        sortcode = random.randint(100000, 999999)
        account_number = random.randint(10000000, 99999999)
        iban = account['account_number']['iban'][:-14] + str(sortcode) + str(account_number)


        # establish session with neo4j
        with self.driver.session(database=self.database) as self.session:
            print(account)
            query = "MERGE (a:Account {id: '%s'})\n" % account['account_id']

            # common across cards and accounts
            query += "SET a.type = 'Bank Account'\n"
            query += "SET a.currency = '%s'\n" % account['currency']
            query += "SET a.provider_display_name = '%s'\n" % account['provider']['display_name']
            query += "SET a.provider_id = '%s'\n" % account['provider']['provider_id']

            # unique to a account
            query += "SET a.account_type = '%s'\n" % account['account_type']
            query += "SET a.display_name = '%s'\n" % account['display_name'].strip()
            query += "SET a.iban = '%s'\n" % iban
            query += "SET a.swift_bic = '%s'\n" % account['account_number']['swift_bic']
            query += "SET a.account_number = '%s'\n" % (account_number)
            query += "SET a.sort_code = '%s'\n" % sortcode

            self.session.run(query)
        self.driver.close()

    def write_cards(self, card):
        # establish session with neo4j
        with self.driver.session(database=self.database) as self.session:
            print(card)
            query = "MERGE (c:Card {id: '%s'})\n" % card['account_id']

            # common across cards and accounts
            query += "SET c.type = 'Credit Card'\n"
            query += "SET c.currency = '%s'\n" % card['currency']
            query += "SET c.provider_display_name = '%s'\n" % card['provider']['display_name']
            query += "SET c.provider_id = '%s'\n" % card['provider']['provider_id']

            # unique to a card
            query += "SET c.card_network = '%s'\n" % card['card_network']
            query += 'SET c.card_type = "%s"\n' % card['card_type']
            query += "SET c.display_name = '%s'\n" % card['display_name']
            query += "SET c.partial_card_number = '%s'\n" % card['partial_card_number']
            query += "SET c.name_on_card = '%s'\n" % card['name_on_card']
            query += "SET c.update_timestamp = datetime('%s')\n" % card['update_timestamp']

            self.session.run(query)
        self.driver.close()

    # write nodes and relationships to neo4j
    def write_transactions(self, transactions, account):
        # establish session with neo4j
        with self.driver.session(database=self.database) as self.session:
            for transaction in transactions:
                print(account + ' | ' + transaction['transaction_id'] + ' | ' + transaction['timestamp'] + ' | ' +
                      transaction['description'] + ' | ' + str(transaction['amount']))

                query = "MATCH (c:Customer) WHERE c.id = 1\n"
                query += "MATCH (a) WHERE (a:Account OR a:Card) AND a.id = '%s'\n" % account
                query += "MERGE (c)-[:HAS_ACCOUNT]->(a)\n"
                query += "MERGE (b:Transactions {id: '%s'})\n" % account
                query += "MERGE (a)-[:HAS_TRANSACTIONS]->(b)\n"

                # create transaction
                query += "MERGE (t:Transaction {transaction_id: '%s'})\n" % transaction['transaction_id']
                query += "SET t.timestamp = datetime('%s')\n" % transaction['timestamp']
                query += 'SET t.description = "%s"\n' % transaction['description']
                query += "SET t.transaction_type = '%s'\n" % transaction['transaction_type']
                query += "SET t.transaction_classification = %s\n" % transaction['transaction_classification']
                query += "SET t.amount = %s\n" % transaction['amount']
                query += "SET t.currency = '%s'\n" % transaction['currency']

                if 'meta' in transaction and 'provider_merchant_name' in transaction['meta']:
                    query += 'SET t.provider_merchant_name = "%s"\n' % transaction['meta']['provider_merchant_name']

                if 'merchant_name' in transaction:
                    query += 'SET t.merchant_name = "%s"\n' % transaction['merchant_name']
                else:
                    if 'meta' in transaction and 'provider_merchant_name' in transaction['meta']:
                        query += 'SET t.merchant_name = "%s"\n' % transaction['meta']['provider_merchant_name']

                query += "MERGE (b)-[:TRANSACTION]->(t);\n"

                self.session.run(query)
        self.driver.close()

    def set_up(self):
        # establish session with neo4j
        with self.driver.session(database=self.database) as self.session:
            query = self.my_node
            self.session.run(query)
        self.driver.close()

from datetime import datetime, timedelta

from load import Load
from truelayer import Truelayer

import os
from configparser import ConfigParser

env = os.getenv("ENV", ".config")

if env == ".config":
    config = ConfigParser()
    config.read(".config")
    config = config["TRUELAYER"]

TRUELAYER_TOKEN = config["TRUELAYER_TOKEN"]
START_DATE = '2023-01-01'


def add_month(date):
    # Parse the date string into a datetime object
    parsed_date = datetime.strptime(date, '%Y-%m-%d')

    # Add one month to the parsed date
    # Since there are different numbers of days in each month, we'll use timedelta
    # to handle this correctly.
    next_month = parsed_date.replace(day=1) + timedelta(days=32)

    # Set the day to 1 to make sure we get the first day of the next month
    result_date = next_month.replace(day=1)

    # Format the result date back to a string if needed
    result_date_str = result_date.strftime('%Y-%m-%d')

    # Get the current date as a datetime object
    current_date = datetime.now()

    # Compare the input date with the current date
    if result_date > current_date:
        # If the input date is greater, set it to the current date
        result_date_str = current_date

        # Convert the updated datetime object back to the 'YYYY-MM-DD' format
        result_date_str = result_date_str.strftime('%Y-%m-%d')

    return result_date_str


def format_transactions(transactions):
    formatted_transcations = []
    # loop over each transaction
    for transaction in transactions:

        # remove fields
        transaction.pop('provider_transaction_id')
        transaction.pop('normalised_provider_transaction_id')
        transaction.pop('transaction_category')

        # remove more fields for credit card payment
        if transaction['description'] == 'PAYMENT RECEIVED - THANK YOU':
            transaction.pop('meta')

        formatted_transcations.append(transaction)

    return formatted_transcations


if __name__ == "__main__":
    # set starting dates
    start_date = START_DATE
    end_date = add_month(START_DATE)

    truelayer = Truelayer()
    load = Load()

    # create my own node
    load.set_up()

    all_banks = truelayer.get_banks(TRUELAYER_TOKEN)

    for bank in all_banks:
        print(bank)
        # get all accounts from bank
        accounts = truelayer.get_accounts(truelayer_token=TRUELAYER_TOKEN, account_id=bank['id'])
        if accounts is not None:
            for account in accounts:
                # print(account)
                load.write_accounts(account=account)

                # set starting dates
                start_date = START_DATE
                end_date = add_month(START_DATE)
                # loop through months until all transactions have been downloaded
                while start_date != datetime.now().strftime('%Y-%m-%d'):
                    # get all transactions for month
                    truelayer_response = truelayer.get_account_transactions(
                        truelayer_token=TRUELAYER_TOKEN,
                        start_date=start_date,
                        end_date=end_date,
                        bank_id=bank['id'],
                        card_id=account['account_id']
                    )

                    if truelayer_response is not None:

                        transactions = format_transactions(truelayer_response['transactions'])

                        print('###')
                        print(f'Start Date: {start_date}')
                        print(f'Number of transactions: {len(transactions)}')
                        print('')

                        if len(transactions) > 0:
                            load.write_transactions(transactions=transactions, account=account['account_id'])

                    # increment dates
                    start_date = add_month(start_date)
                    end_date = add_month(end_date)

        # get all cards from banks
        cards = truelayer.get_all_cards(truelayer_token=TRUELAYER_TOKEN, card_id=bank['id'])
        for card in cards:
            # print(card)
            load.write_cards(card)

            # set starting dates
            start_date = START_DATE
            end_date = add_month(START_DATE)
            # loop through months until all transactions have been downloaded
            while start_date != datetime.now().strftime('%Y-%m-%d'):
                # get all transactions for month
                truelayer_response = truelayer.get_card_transactions(
                    truelayer_token=TRUELAYER_TOKEN,
                    start_date=start_date,
                    end_date=end_date,
                    bank_id=bank['id'],
                    card_id=card['account_id']
                )

                if truelayer_response is not None:

                    transactions = format_transactions(truelayer_response['transactions'])

                    print('###')
                    print(f'Start Date: {start_date}')
                    print(f'Number of transactions: {len(transactions)}')
                    print('')

                    if len(transactions) > 0:
                        load.write_transactions(transactions=transactions, account=card['account_id'])

                # increment dates
                start_date = add_month(start_date)
                end_date = add_month(end_date)

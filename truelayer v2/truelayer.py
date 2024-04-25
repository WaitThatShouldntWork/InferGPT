import requests


class Truelayer:
    def __init__(self):
        self.BANK_URI = "https://demo-api.truelayer.com/banks"

    def get_banks(self, truelayer_token):
        url = self.BANK_URI
        headers = {
            'Authorization': f'Bearer {truelayer_token}'
        }

        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            return data
        else:
            print(f"Failed with status code: {response.status_code}")

    def get_accounts(self, truelayer_token, account_id):
        url = self.BANK_URI + '/' + account_id + '/accounts'
        headers = {
            'Authorization': f'Bearer {truelayer_token}'
        }

        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            return data
        else:
            print(url)
            print(f"Failed with status code: {response.status_code}")

    def get_account_transactions(self, truelayer_token, start_date, end_date, bank_id, card_id):
        url = self.BANK_URI + '/' + bank_id + '/accounts/' + card_id + '/transactions'
        headers = {
            'Authorization': f'Bearer {truelayer_token}'
        }

        params = {
            'fromDate': start_date,
            'toDate': end_date
        }

        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            return data
        else:
            print(url)
            print(params)
            print(f"Failed with status code: {response.status_code}")

    def get_all_cards(self, truelayer_token, card_id):
        url = self.BANK_URI + '/' + card_id + '/cards'
        headers = {
            'Authorization': f'Bearer {truelayer_token}'
        }

        response = requests.get(url, headers=headers)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            return data
        else:
            print(url)
            print(f"Failed with status code: {response.status_code}")

    def get_card_transactions(self, truelayer_token, start_date, end_date, bank_id, card_id):
        url = self.BANK_URI + '/' + bank_id + '/cards/' + card_id + '/transactions'
        headers = {
            'Authorization': f'Bearer {truelayer_token}'
        }

        params = {
            'fromDate': start_date,
            'toDate': end_date
        }

        response = requests.get(url, headers=headers, params=params)

        # Check if the request was successful (status code 200)
        if response.status_code == 200:
            data = response.json()
            # Process the data as needed
            return data
        else:
            print(url)
            print(params)
            print(f"Failed with status code: {response.status_code}")

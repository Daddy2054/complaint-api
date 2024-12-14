import json
import os
import uuid
import dotenv
import requests

dotenv.load_dotenv()

wise_token = os.getenv("WISE_TOKEN")
wise_url = os.getenv("WISE_URL")


class WiseService:
    def __init__(self):
        self.main_url = wise_url
        self.headers = {
            "Content-type": "application/json",
            "Authorization": f"Bearer {wise_token}",
        }

        self.profile_id = self._get_profile_id()

    #       print(self.profile_id)

    def _get_profile_id(self):
        url = f"{self.main_url}/v2/profiles"
        response = requests.get(url, headers=self.headers)
        if response.status_code == 200:
            profile_id = response.json()[0]["id"]
            return profile_id
        else:
            raise Exception("Could not get profile id")

    def create_quote(self, amount):
        url = f"{self.main_url}/v2/quotes"
        data = {
            "sourceCurrency": "EUR",
            "targetCurrency": "EUR",
            "sourceAmount": amount,
            "profile": self.profile_id,
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()["id"]

    def create_recipient_account(self, full_name, iban):
        url = f"{self.main_url}/v1/accounts"
        data = {
            "currency": "EUR",
            "type": "iban",
            "profile": self.profile_id,
            "accountHolderName": full_name,
            "legalType": "PRIVATE",
            "details": {"iban": iban},
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            return response.json()["id"]
        else:
            raise Exception("Could not create recipient acccount")

    def transfer(self, target_account_id, quote_id):
        url = f"{self.main_url}/v1/transfers"
        customer_transaction_id = str(uuid.uuid4())
        data = {
            "targetAccount": target_account_id,
            "quoteUuid": quote_id,
            "customerTransactionId": customer_transaction_id,
            "details": {"reference": "Transfer to account"},
        }
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 200:
            # print(response.json())
            #return True
            return response.json()["id"]
        else:
            raise Exception("Could not transfer")

    def fund_transfer(self, transfer_id):
        url = f"{self.main_url}/v3/profiles/{self.profile_id}/transfers/{transfer_id}/payments"
        data = {"type": "BALANCE"}
        response = requests.post(url, headers=self.headers, json=data)
        if response.status_code == 201:
            #print(response.content)
            return json.loads(response.content)
        else:
            print(json.loads(response.content))
            raise Exception("Could not transfer")


    def cancel_transfer(self, transfer_id):
        url = f"{self.main_url}/v1/transfers/{transfer_id}/cancel"
        response = requests.put(url, headers=self.headers)
        if response.status_code == 200:
            return True
        else:
            raise Exception("Could not cancel transfer")
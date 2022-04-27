#based on https://pyteal.readthedocs.io/en/latest/examples.html#voting
#which is based on https://github.com/algorand/docs/blob/cdf11d48a4b1168752e6ccaf77c8b9e8e599713a/examples/smart_contracts/v2/python/stateful_smart_contracts.py

import base64

from algosdk.future import transaction
from algosdk import account, mnemonic
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
from smart_contract import programMaker
import json



f = open("accounts.json")
jsonDict = json.load(f)
accounts = jsonDict["accounts"]
# user declared algod connection parameters
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

params = algod_client.suggested_params()

def create_application():
    
    #make sender
    sender = accounts[0]['address']

    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        programMaker,
    )


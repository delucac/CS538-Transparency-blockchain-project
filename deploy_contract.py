#based on https://pyteal.readthedocs.io/en/latest/examples.html#voting
#which is based on https://github.com/algorand/docs/blob/cdf11d48a4b1168752e6ccaf77c8b9e8e599713a/examples/smart_contracts/v2/python/stateful_smart_contracts.py

import base64

from algosdk.future import transaction
from algosdk import account, mnemonic
from algosdk.v2client import algod
from pyteal import compileTeal, Mode
from smart_contract import programMaker
from pyteal import *
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
    local_ints = 100
    local_bytes = 100
    global_ints = 100
    global_bytes = 100
    global_schema = transaction.StateSchema(global_ints, global_bytes)
    local_schema = transaction.StateSchema(local_ints, local_bytes)
    sender = accounts[0]['address']
    pk = accounts[0]['key']
    txn = transaction.ApplicationCreateTxn(
        sender,
        params,
        programMaker(),
        programMaker(),
        programMaker(),
        global_schema,
        local_schema
    )
    signedtxn=txn.sign(pk)
    txid = signedtxn.get_txid()
    algod_client.send_transaction([signedtxn])
    wait_for_confirmation(algod_client, txid)
    transaction_response = algod_client.pending_transaction_info(txid)
    app_id = transaction_response["application-index"]
    print("Created new app-id:", app_id)

def wait_for_confirmation(client, txid):
    last_round = client.status().get("last-round")
    txinfo = client.pending_transaction_info(txid)
    while not (txinfo.get("confirmed-round") and txinfo.get("confirmed-round") > 0):
        print("Waiting for confirmation...")
        last_round += 1
        client.status_after_block(last_round)
        txinfo = client.pending_transaction_info(txid)
    print(
        "Transaction {} confirmed in round {}.".format(
            txid, txinfo.get("confirmed-round")
        )
    )
    return txinfo


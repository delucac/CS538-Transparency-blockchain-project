import json
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account
from algosdk.future.transaction import *

f = open("accounts.json")
jsonDict = json.load(f)
# user declared algod connection parameters
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

params = algod_client.suggested_params()
accounts = jsonDict["accounts"]
txn = AssetConfigTxn(
    sender=accounts[0]['address'],
    sp=params,
    total=100,
    default_frozen=False,
    unit_name="Note",
    asset_name="notes",
    manager=accounts[0]['address'],
    reserve=accounts[0]['address'],
    freeze=accounts[0]['address'],
    clawback=accounts[0]['address'],
    decimals=0)
# Sign with secret key of creator
stxn = txn.sign(accounts[0]['key'])
# Send the transaction to the network and retrieve the txid.
try:
    txid = algod_client.send_transaction(stxn)
    print("Signed transaction with txID: {}".format(txid))
    # Wait for the transaction to be confirmed
    confirmed_txn = wait_for_confirmation(algod_client, txid, 4)  
    print("TXID: ", txid)
    print("Result confirmed in round: {}".format(confirmed_txn['confirmed-round']))   
except Exception as err:
    print(err)
# Retrieve the asset ID of the newly created asset by first
# ensuring that the creation transaction was confirmed,
# then grabbing the asset id from the transaction.
print("Transaction information: {}".format(
    json.dumps(confirmed_txn, indent=4)))
# print("Decoded note: {}".format(base64.b64decode(
#     confirmed_txn["txn"]["txn"]["note"]).decode()))
try:
    # Pull account info for the creator
    # account_info = algod_client.account_info(accounts[1]['pk'])
    # get asset_id from tx
    # Get the new asset's information from the creator account
    ptx = algod_client.pending_transaction_info(txid)
    asset_id = ptx["asset-index"]
    jsonDict['asset_id'] = asset_id
except Exception as e:
    print(e)
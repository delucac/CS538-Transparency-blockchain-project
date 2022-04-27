#based off first_trnx.py
import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction

f = open("accounts.json")
jsonDict = json.load(f)

private_key = jsonDict["accounts"][1]['address']

#connection parameters
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

def contract_optIn(private_key, my_address):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = ApplicationOptInTxn(sender, params, 85862110)
    
    #sign
    signed_txn = unsigned_txn.sign(private_key)
    tx_id = signed_txn.transaction,get_txid()
    
    #send
    client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        
def contract_requestNotes(private_key):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = ApplicationNoOpTxn(sender, params, 85862110, "Request")
    
    #sign
    signed_txn = unsigned_txn.sign(private_key)
    tx_id = signed_txn.transaction,get_txid()
    
    #send
    client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        


def contract_returnNotes():
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = ApplicationNoOpTxn(sender, params, 85862110, "Return")
    
    #sign
    signed_txn = unsigned_txn.sign(private_key)
    tx_id = signed_txn.transaction,get_txid()
    
    #send
    client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        
    
def contract_startMeeting():
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = ApplicationNoOpTxn(sender, params, 85862110, "Start")
    
    #sign
    signed_txn = unsigned_txn.sign(private_key)
    tx_id = signed_txn.transaction,get_txid()
    
    #send
    client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        
    
def contract_stopMeeting():
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = ApplicationNoOpTxn(sender, params, 85862110, "Stop")
    
    #sign
    signed_txn = unsigned_txn.sign(private_key)
    tx_id = signed_txn.transaction,get_txid()
    
    #send
    client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, txid, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        

#based off first_trnx.py
import json
import base64
from algosdk import account, mnemonic, constants
from algosdk.v2client import algod
from algosdk.future import transaction


f = open("accounts.json")
jsonDict = json.load(f)

private_key = jsonDict["accounts"][1]['key']

#connection parameters
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)
appID = jsonDict["app_id"]
def contract_optIn(private_key, my_address):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = transaction.ApplicationOptInTxn(sender, params, appID)
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        
def contract_requestNotes(private_key):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = transaction.ApplicationNoOpTxn(sender, params, appID, "Request")
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        


def contract_returnNotes(private_key):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = transaction.ApplicationNoOpTxn(sender, params, appID, "Return")
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

def contract_startMeeting(private_key):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = transaction.ApplicationNoOpTxn(sender, params, appID, "Start")
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))
        
    
def contract_stopMeeting(private_key):
    #Make transaction
    params = algod_client.suggested_params()
    sender = account.address_from_private_key(private_key)
    txn = transaction.ApplicationNoOpTxn(sender, params, appID, "Stop")
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

def contract_whiteList(private_key, private_key2):
    #Make transaction
    params = algod_client.suggested_params()
    account1 = account.address_from_private_key(private_key)
    account2 = account.address_from_private_key(private_key2)
    accountList = []
    accountList.append(account1)
    accountList.append(account2)
    txn = transaction.ApplicationNoOpTxn(accountList, params, appID, "Whitelist")
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))


def contract_admin(private_key, private_key2):
    #Make transaction
    params = algod_client.suggested_params()
    account1 = account.address_from_private_key(private_key)
    account2 = account.address_from_private_key(private_key2)
    accountList = []
    accountList.append(account1)
    accountList.append(account2)
    txn = transaction.ApplicationNoOpTxn(accountList, params, appID, "Admin")
    
    #sign
    signed_txn = txn.sign(private_key)
    tx_id = signed_txn.transaction.get_txid()
    
    #send
    algod_client.send_transactions([signed_txn])
    
    # wait for confirmation
    try:
        confirmed_txn = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    except Exception as err:
        print(err)
        return
        
    print("Transaction information: {}".format(
        json.dumps(confirmed_txn, indent=4)))

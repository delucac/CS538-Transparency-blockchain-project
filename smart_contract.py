from email.headerregistry import Address
import json
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account
from algosdk.future.transaction import *
from pyteal import *
from sympy import SeqAdd

f = open("accounts.json")
jsonDict = json.load(f)
# user declared algod connection parameters
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

params = algod_client.suggested_params()
def program():

    WHITELISTED_KEY = Bytes("whitelisted")
    ADMIN_KEY = Bytes("admin") 

    is_contract_admin = App.localGet(Int(0), ADMIN_KEY)
    is_whitelisted = App.localGet(Int(0),WHITELISTED_KEY)


    handle_creation = Seq(
    App.globalPut(Bytes("Meeting #"),
    Int(0)),
    App.localPut(Int(0),ADMIN_KEY, Int(1)),
    Return(Int(1))
    )
    
    #Starts as not Whitelisted
    handle_optin = Seq(
           App.localPut(Int(0), WHITELISTED_KEY, Int(0)), Return(Int(1)) 
    )


    scratchCount = ScratchVar(TealType.uint64)
    #Create counter so that each meeting can be tracked in order.
    counter = Seq(scratchCount.store(App.globalGet(Bytes("Meeting #"))),
    App.globalPut(Bytes("Meeting #"), scratchCount.load()+Int(1)),
    Return(Int(1))
    )
    #Allows someone to use the smart contract must be done by someone who is currently an admin
    whitelist = Seq(
        [
            Assert(
                And(
                    is_contract_admin,
                    Txn.application_args.length() == Int(2),
                    Txn.accounts.length() == Int(1)
                )
            ),
            App.localPut(Int(1), WHITELISTED_KEY, Int(1)),
            Return(Int(1))
        ]
    )
    makeAdmin = Seq(
        [
             Assert(
                And(
                    is_contract_admin,
                    Txn.application_args.length() == Int(2),
                    Txn.accounts.length() == Int(1)
                )
            ),
            App.localPut(Int(1), ADMIN_KEY, Int(1)),
            Return(Int(1))
        ]
    )
    
    #Additions
    
    #based on https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/#asset-transfer
    #used to send notes asset to user
    distribute = Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
        	TxnField.type_enum: TxnType.AssetTransfer,
        	TxnField.asset_sender: ("PH4LOMJTTIZJCH7F2HCAMXVEA4B34ZQ4A5B4BERSAGT25C7XK3R4SOFTG4"),
        	TxnField.asset_receiver: Txn.Sender(),
        	TxnField.asset_amount: Int(1),
        	TxnField.xfer_asset(85862110)
       }),
       InnerTxnBuilder.Submit()
    )
    
    #Used to reclaim note asset
    retrieveNote = Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
        	TxnField.type_enum: TxnType.AssetTransfer,
        	TxnField.asset_sender: Txn.Sender(),
        	TxnField.asset_receiver: ("PH4LOMJTTIZJCH7F2HCAMXVEA4B34ZQ4A5B4BERSAGT25C7XK3R4SOFTG4"),
        	TxnField.asset_amount: Int(1),
        	TxnField.xfer_asset(85862110)
       }),
       InnerTxnBuilder.Submit()
    )
    
    
    
    #based on https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/#call-the-smart-contract
    #Found better if statement setup with Cond, based on PyTeal docs
    request_notes = Seq(
    	distribute(),
    	Return(Int(1))
    )
    return_notes = Seq(
        retrieveNote(),
        Return(Int(1))
    )
    meeting_start = Seq(
        Return(Int(1))
    )
    meeting_stop = Seq(
        Return(Int(1))
    )
    
    checkRequest = Cond(
         [Bytes("Start") == Txn.application_args[0], meeting_start],
         [Bytes("Stop") == Txn.application_args[0], meeting_stop],
         [Bytes("Request") == Txn.application_args[0], request_notes],
         [Bytes("Return") == Txn.application_args[0], return_notes]
         )

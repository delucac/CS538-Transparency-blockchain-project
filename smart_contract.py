
import json
import base64
from algosdk.v2client import algod
from algosdk import mnemonic
from algosdk import account
from algosdk.future.transaction import *
from pyteal import *


f = open("accounts.json")
jsonDict = json.load(f)
# user declared algod connection parameters
algod_address = "http://localhost:4001"
algod_token = "aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
algod_client = algod.AlgodClient(algod_token, algod_address)

params = algod_client.suggested_params()
def programMaker():

    WHITELISTED_KEY = Bytes("whitelisted")
    ADMIN_KEY = Bytes("admin") 
    ONGOING = Bytes("ongoing")
    MEETINGCOUNTER= Bytes("Meeting #")
    is_contract_admin = App.localGet(Int(0), ADMIN_KEY) 
    is_whitelisted = App.localGet(Int(0),WHITELISTED_KEY)
    is_ongoing = App.globalGet(ONGOING)

    handle_creation = Seq(
    App.globalPut(MEETINGCOUNTER, Int(0)),
    App.globalPut(ONGOING,Int(0)),
    Return(Int(1))
    )
    
    #Starts as not Whitelisted
    handle_optin = Seq(
           App.localPut(Int(0), WHITELISTED_KEY, Int(0)), Return(Int(1)) 
    )


    scratchCount = ScratchVar(TealType.uint64)
    #Create counter so that each meeting can be tracked in order.
    counter = Seq(scratchCount.store(App.globalGet(MEETINGCOUNTER)),
    App.globalPut(MEETINGCOUNTER, scratchCount.load()+Int(1)),
    Return(Int(1))
    )
    #Allows someone to use the smart contract must be done by someone who is currently an admin
    whitelist = Seq(
        [
            Assert(
                Or(
                And(
                    is_contract_admin,
                    #Txn.application_args.length() == Int(2),
                    Txn.accounts.length() == Int(1)
                ),
                And
                (
                    #Txn.application_args.length()==Int(2)
                    Txn.accounts.length() == Int(0),
                    Txn.sender()==Bytes(jsonDict["accounts"][0]["address"])
                )
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
                    #Txn.application_args.length() == Int(2),
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
        	TxnField.asset_sender: Global.current_application_address(),
        	TxnField.asset_receiver: Txn.sender(),
        	TxnField.asset_amount: Int(1),
        	TxnField.xfer_asset : Int(jsonDict["note_id"])
       }),
       InnerTxnBuilder.Submit()
    )
    
    #Used to reclaim note asset
    retrieveNote = Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
        	TxnField.type_enum: TxnType.AssetTransfer,
        	TxnField.asset_sender: Txn.sender(),
        	TxnField.asset_receiver: Global.current_application_address(),
        	TxnField.asset_amount: Int(1),
        	TxnField.xfer_asset : Int(jsonDict["note_id"])
       }),
       InnerTxnBuilder.Submit()
    )
    #TODO send transaction dictating start of meeting with a token to itself
    startMeeting = Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
        	TxnField.type_enum: TxnType.AssetTransfer,
        	TxnField.asset_sender: Global.current_application_address(),
        	TxnField.asset_receiver: Global.current_application_address(),
        	TxnField.asset_amount: Int(1),
        	TxnField.xfer_asset : Int(jsonDict["asset_id"]),
            TxnField.note : Concat(Bytes("Starting meeting: "),
            App.globalGet(Bytes("Meeting #")))
       }),
       InnerTxnBuilder.Submit(),
       App.globalPut(Bytes("Ongoing"),Int(1))
    )
    #TODO send transaction dictating end of meeting with a token to itself
    stopMeeting = Seq(
        InnerTxnBuilder.Begin(),
        InnerTxnBuilder.SetFields({
        	TxnField.type_enum: TxnType.AssetTransfer,
        	TxnField.asset_sender: Global.current_application_address(),
        	TxnField.asset_receiver: Global.current_application_address(),
        	TxnField.asset_amount: Int(1),
        	TxnField.xfer_asset : Int(jsonDict["asset_id"]),
            TxnField.note: Concat(Bytes("Ending meeting: "),App.globalGet(Bytes("Meeting #"))),
       }),
       InnerTxnBuilder.Submit(),
       counter,
       App.globalPut(Bytes("Ongoing"),Int(0))
    )
    
    #based on https://developer.algorand.org/docs/get-details/dapps/smart-contracts/apps/#call-the-smart-contract
    #Found better if statement setup with Cond, based on PyTeal docs
    request_notes = Seq(
        Assert(
                And(
        is_whitelisted,
        is_ongoing)
        ),
    	distribute,
    	Return(Int(1))
    )
    return_notes = Seq(
        Assert(
        is_whitelisted),
        retrieveNote,
        Return(Int(1))
    )
    meeting_start = Seq(
        Assert(
        is_contract_admin),
        startMeeting,
        Return(Int(1))
    )
    meeting_stop = Seq(
        Assert(
        is_contract_admin),
    	stopMeeting,
        Return(Int(1))
    )
    
    handle_noop = Cond(
         [Bytes("Start") == Txn.application_args[0], meeting_start],
         [Bytes("Stop") == Txn.application_args[0], meeting_stop],
         [Bytes("Request") == Txn.application_args[0], request_notes],
         [Bytes("Return") == Txn.application_args[0], return_notes],
         [Bytes("Whitelist")==Txn.application_args[0], whitelist],
         [Bytes("Admin")==Txn.application_args[0],makeAdmin]
         )
    program = Cond(
        [Txn.application_id()== Int(0), handle_creation],
        [Txn.on_completion() == OnComplete.NoOp, handle_noop],
        [Txn.on_completion() == OnComplete.OptIn, handle_optin],
        )
    return program
with open('MeetingContract.teal','w') as f:
    compiled = compileTeal(programMaker(),Mode.Application,version=6)
    f.write(compiled)

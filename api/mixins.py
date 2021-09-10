from datetime import datetime, date, time, timedelta
from django.conf import settings
from users.models import UserProfile
from api.models import Invoicing
from .get_client import client, OPERATOR_ID, OPERATOR_KEY, config_user_client
import time

from hedera import (
    Hbar,
    AccountId,
    PrivateKey,
    Client,
    AccountBalanceQuery,
    TransferTransaction,
    AccountCreateTransaction
    )



class UserClientMixin:

	def __init__(self, *args, **kwargs):
		self.user = kwargs.get("user")
		self.up = self.user.userprofile
		self.amount = kwargs.get("amount")
		self.description = kwargs.get("description")
		#call config_user_client to make a transaction
		self.client = config_user_client(self.user)





class HederaAccount:
	'''
	Manages the creation of a Hedera user account
	'''

	def __init__(self, user):

		self.user = user				
		self.private = PrivateKey.generate()
		self.public = self.private.getPublicKey()

		tran = AccountCreateTransaction()

		# need a certain number of hbars, otherwise it can not be deleted later
		resp = tran.setKey(self.public).setInitialBalance(Hbar(1000)).execute(client)
		receipt = resp.getReceipt(client)

		acc_id = receipt.accountId.toString()
		up = self.user.userprofile
		up.acc = acc_id
		up.pubkey = self.public.toString()
		up.privatekey = self.private.toString()
		up.save()




class HederaPayment(UserClientMixin):


	def create(self):

		#convert millibar to tinybar
		tinybar_conversion = int(self.amount) * 100_000

		amount = Hbar.fromTinybars(int(tinybar_conversion))
		acc_id = AccountId.fromString(self.up.acc)
		
		resp = TransferTransaction(
		       ).addHbarTransfer(acc_id, amount.negated()
		       ).addHbarTransfer(OPERATOR_ID, amount
		       ).setTransactionMemo(self.description
		       ).execute(self.client) # notice that we are using self.client from __init_ the transaction must have the sender signiture!!

		status = resp.getReceipt(self.client).status.toString()

		tran_id = resp.getRecord(self.client).transactionId

		if status == "SUCCESS":
			message = "Perfect"
			return {"message": message, "tran_id": tran_id.toString()}

		else:
			message = "Something went wrong"
			return {"message": message}

		


class HederaData(UserClientMixin):

	'''
	Produces and returns a list of cards assigned to each user
	'''
	def balance(self):

		acc_id = AccountId.fromString(self.up.acc)
		balance = AccountBalanceQuery().setAccountId(acc_id).execute(self.client).hbars.toString()		
		return balance
		



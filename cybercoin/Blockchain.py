"""
Copyright (C) 2023  Miles Rack

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""
from decimal import Decimal
from .Block import Block
import datetime
from .Cryptography import sha256_hash
import json
import random
from .Wallet import Wallet

class Blockchain:
	def __init__(self):
		self.unconfirmed_transactions = []
		self.blocks = []
		self.wallets = {}
		self.difficulty = 4
		self.fee = Decimal("0.00")
		self.vault_ = self.new_wallet()
		self.vault_.balance = Decimal("Infinity")
		self.create_genesis()

	def create_genesis(self):
		genesis = Block(0, "0"*64)
		transaction = {
			"txid":"",
			"timestamp":str(datetime.datetime.now()),
			"sender":f"0x{'0'*32}",
			"recipient":self.vault_.address,
			"amount":str(Decimal("1000.00")),
			"fee":str(Decimal("0.00"))
		}
		transaction["txid"] = sha256_hash(json.dumps(transaction))
		genesis.data = transaction
		#print(f"[+] Coinbase transaction: {transaction}")
		#print("[+] Mining genesis block...")
		mined = False
		while not mined:
			nonce = int("".join([str(random.randint(0,9)) for i in range(8)]))
			genesis.nonce = nonce
			new_hash = genesis.hash()
			if new_hash.startswith("0"*self.difficulty):
				recipient = self.wallet(transaction["recipient"])
				recipient.balance += Decimal(transaction["amount"])
				mined = True		
				#print(f"[+] Mined block #{genesis.index}")
				#print(f"[+] Nonce: {genesis.nonce}")
				#print(f"[+] Hash: {genesis.hash()}")
				#print(f"[+] Data: {genesis.data}")
		self.blocks.append(genesis)
	
	def new_wallet(self):
		unique = False
		while not unique:
			wallet = Wallet()
			unique = wallet.address not in self.wallets.keys()
		self.wallets[wallet.address] = wallet
		return wallet

	def wallet(self, address):
		if address in self.wallets.keys():
			return self.wallets[address]
		return False

	def vault(self):
		return self.vault_

	def get_wallets(self):
		wallets = {address:str(wallet.balance) for (address, wallet) in self.wallets.items()}
		#return {"success":True, "message":"", "data":wallets}
		return wallets

	def get_wallet(self, address):
		wallet = self.wallet(address)
		if wallet:
			#return {"success":True, "message":"", "data":wallet.__dict__}
			return wallet.__dict__
		#return {"success":False, "message":"Wallet does not exists", "data":""}
		return False

	def length(self):
		return len(self.blocks)

	def get_blocks(self):
		blockchain = {block.index:block.__dict__ for block in self.blocks}
		#return {"success":True, "message":"", "data":blockchain}
		return blockchain

	def get_block(self, index):
		if 0 <= index < len(self.blocks):
			#return {"success":True, "message":"", "data":self.blocks[index].__dict__}
			return self.blocks[index].__dict__
		#return {"success":False, "message":"Invalid block index", "data":""}
		return False

	def last_block(self):
		return self.blocks[-1]

	def get_difficulty(self):
		return self.difficulty

	def set_difficulty(self, difficulty):
		try:
			assert 0 <= difficulty < 64
			self.difficulty = int(difficulty)
		except:
			return False
		else:
			return True

	def get_fee(self):
		return str(self.fee)

	def set_fee(self, fee):
		try:
			self.fee = Decimal(str(fee))
		except:
			return False
		else:
			return True

	def get_transactions(self, address=None):
		transactions = []
		for block in self.blocks:
			data = block.data
			if (data["sender"] == address or data["recipient"] == address) or not address:
				transactions.append(data)
		#return {"success": True, "message":"", "data":transactions}
		return transactions

	def get_transaction(self, txid):
		for block in self.blocks:
			if block.data["txid"] == txid:
				#return {"success":True, "message":"", "data":block.data}
				return block.data
		#return {"success":False, "message":"Invalid txid", "data":""}
		return False

	def new_transaction(self, sender, recipient, amount):
		amount = Decimal(str(amount))
		if amount <= Decimal('0'):
			#return {"success":False, "message":"Amount must be greater than 0", "data":""}
			return False
		if not sender:
			#return {"success":False, "message":"Invalid sender wallet", "data":""}
			return False
		if not recipient:
			#return {"success":False, "message":"Invalid recipient wallet", "data":""}
			return False
		if sender.balance - (amount + amount * self.fee) < Decimal('0'):
			#return {"success":False, "message":f"Insufficient balance (network fee: {self.fee})", "data":""}
			return False
		sender.balance -= amount + amount * self.fee
		transaction = {
			"txid":"",
			"timestamp":str(datetime.datetime.now()),
			"sender":sender.address,
			"recipient":recipient.address,
			"amount":str(amount),
			"fee":str(amount * self.fee)
		}
		transaction["txid"] = sha256_hash(json.dumps(transaction))
		self.unconfirmed_transactions.append(transaction)
		#print(f"[+] New transaction: {transaction}")
		#return {"success":True, "message":f"Sent {str(amount)} CYB from {sender.address} => {recipient.address}", "data":transaction}
		return transaction

	def mine(self):
		if self.unconfirmed_transactions:
			transaction = self.unconfirmed_transactions.pop(0)
			last_block = self.last_block()
			block = Block(last_block.index + 1, last_block.hash())
			block.data = transaction
			#print("[+] Mining block...")
			mined = False
			while not mined:
				nonce = int("".join([str(random.randint(0,9)) for i in range(8)]))
				block.nonce = nonce
				new_hash = block.hash()
				if new_hash.startswith("0"*self.difficulty):
					recipient = self.wallet(transaction["recipient"])
					recipient.balance += Decimal(transaction["amount"])
					self.vault_.balance += Decimal(transaction["fee"])
					mined = True		
					#print(f"[+] Mined block #{block.index}")
					#print(f"[+] Nonce: {block.nonce}")
					#print(f"[+] Hash: {block.hash()}")
					#print(f"[+] Data: {block.data}")
			self.blocks.append(block)

	def validate(self):
		#print("[+] Validating blocks...")
		i = 0
		previous_hash = "0"*64
		#validation = {}
		while i < len(self.blocks):
			block = self.blocks[i]
			#print(f"[+] {previous_hash} => {block.hash()}")
			#validation[i] = f"{previous_hash} => {block.hash()}"
			if block.previous_hash != previous_hash:
				#return {"success":False, "message":f"Block #{block.index}: {block.previous_hash} != {previous_hash}", "data":validation}
				return False
			previous_hash = block.hash()
			i += 1
		#return {"success":True, "message":"All blocks are valid", "data":validation}
		return True

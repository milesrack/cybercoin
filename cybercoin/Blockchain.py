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
import requests
from .Wallet import Wallet

class Blockchain:
	def __init__(self):
		self.unconfirmed_transactions = []
		self.blocks = []
		self.wallets = {}
		self.nodes = set()
		#self.nodes.add("http://127.0.0.1:5000/")
		self.difficulty = 4
		self.fee = Decimal("0.00")
		self.vault_ = self.new_wallet()
		self.vault_.balance = Decimal("Infinity")
		self.create_genesis()

	def create_genesis(self):
		block = Block(0, "0"*64)
		transaction = {
			"txid":"",
			"timestamp":str(datetime.datetime.now()),
			"sender":f"0x{'0'*32}",
			"recipient":self.vault_.address,
			"amount":str(Decimal("1000.00")),
			"fee":str(Decimal("0.00"))
		}
		transaction["txid"] = sha256_hash(json.dumps(transaction))
		block.data = transaction
		#mined = False
		#while not mined:
		#	nonce = int("".join([str(random.randint(0,9)) for i in range(8)]))
		#	block.nonce = nonce
		#	new_hash = block.hash()
		#	if new_hash.startswith("0"*self.difficulty):
		#		recipient = self.wallet(transaction["recipient"])
		#		recipient.balance += Decimal(transaction["amount"])
		#		mined = True		
		#self.blocks.append(block)
		mined = False
		while not mined:
			nonce = int("".join([str(random.randint(0,9)) for i in range(8)]))
			block.nonce = nonce
			new_hash = block.hash()
			if new_hash.startswith("0"*self.difficulty):
				mined = True
				recipient = self.wallet(transaction["recipient"])
				recipient.balance += Decimal(transaction["amount"])
				self.vault_.balance += Decimal(transaction["fee"])
				self.blocks.append(block)
		#blocks_before = self.get_blocks()
		#self.nodes.add("http://127.0.0.1:5000/")
		#self.consensus()
		#if blocks_before == self.get_blocks():
		#	recipient = self.wallet(transaction["recipient"])
		#	recipient.balance += Decimal(transaction["amount"])
		#	self.vault_.balance += Decimal(transaction["fee"])
		#	self.blocks.append(block)
		#	self.announce_block(block)
	
	def timestamp_genesis(self, blocks=None):
		if blocks is None:
			blocks = self.blocks
		return datetime.datetime.fromisoformat(blocks[0].data["timestamp"])	

	def new_wallet(self):
		unique = False
		while not unique:
			wallet = Wallet()
			unique = wallet.address not in self.wallets.keys()
		self.wallets[wallet.address] = wallet
		self.announce_wallet(wallet)
		return wallet

	def wallet(self, address):
		if address in self.wallets.keys():
			return self.wallets[address]
		return False

	def vault(self):
		return self.vault_

	def get_wallets(self):
		wallets = {address:str(wallet.balance) for (address, wallet) in self.wallets.items()}
		return wallets

	def get_wallet(self, address):
		wallet = self.wallet(address)
		if wallet:
			return {key:str(value) for key, value in wallet.__dict__.items()}
		return False

	def length(self):
		return len(self.blocks)

	def get_blocks(self):
		blockchain = {block.index:block.__dict__ for block in self.blocks}
		return blockchain

	def get_block(self, index):
		if 0 <= index < len(self.blocks):
			return self.blocks[index].__dict__
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
		return transactions

	def get_pending(self):
		return self.unconfirmed_transactions

	def get_transaction(self, txid):
		for block in self.blocks:
			if block.data["txid"] == txid:
				return block.data
		return False

	def new_transaction(self, sender, recipient, amount):
		amount = Decimal(str(amount))
		if amount <= Decimal('0'):
			return False
		if not sender:
			return False
		if not recipient:
			return False
		if sender.balance - (amount + amount * self.fee) < Decimal('0'):
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
		return transaction

	def mine(self):
		confirmed = []
		while self.unconfirmed_transactions:
			transaction = self.unconfirmed_transactions.pop(0)
			last_block = self.last_block()
			block = Block(last_block.index + 1, last_block.hash())
			block.data = transaction
			mined = False
			while not mined:
				nonce = int("".join([str(random.randint(0,9)) for i in range(8)]))
				block.nonce = nonce
				new_hash = block.hash()
				if new_hash.startswith("0"*self.difficulty):
					mined = True		
			blocks_before = self.get_blocks()
			self.consensus()
			if blocks_before == self.get_blocks():
				recipient = self.wallet(transaction["recipient"])
				recipient.balance += Decimal(transaction["amount"])
				self.vault_.balance += Decimal(transaction["fee"])
				self.blocks.append(block)
				self.announce_block(block)
				confirmed.append(block.__dict__)
		return confirmed

	def validate(self, blocks=None):
		if blocks is None:
			blocks = self.blocks
		i = 0
		previous_hash = "0"*64
		while i < len(blocks):
			block = blocks[i]
			if (block.previous_hash != previous_hash):
				return False
			previous_hash = block.hash()
			i += 1
		return True

	def get_nodes(self):
		return self.nodes

	def add_nodes(self, urls):
		self.nodes.update(urls)

	def blocks_from_json(self, dump):
		blocks = []
		for index,block in dump.items():
			b = Block()
			b.index = int(block["index"])
			b.previous_hash = block["previous_hash"]
			b.nonce = int(block["nonce"])
			b.data = block["data"]
			blocks.append(b)
		return blocks

	def import_blocks(self, blocks):
		self.blocks = self.blocks_from_json(blocks)
		return True		

	def wallet_from_json(self, wallet):
		w = Wallet()
		w.address = wallet["address"]
		w.balance = Decimal(wallet["balance"])
		return w

	def wallets_from_json(self, wallets):
		new_wallets = {}
		for address, balance in wallets.items():
			wallet = Wallet()
			wallet.address = address
			wallet.balance = Decimal(balance)
			new_wallets[address] = wallet
		return new_wallets

	def import_wallets(self, wallets):
		self.wallets = self.wallets_from_json(wallets)
		return True

	def add_wallet(self, wallet):
		self.wallets.update({wallet.address:wallet})
		return True

	def add_block(self, block):
		if block.index == 0 and datetime.datetime.fromisoformat(block["data"]["timestamp"]) < datetime.datetime.fromisoformat(self.blocks[0].data["timestamp"]):
			self.blocks = [block]
			return True
		elif block.previous_hash == self.last_block().hash():
			self.blocks.append(block)
			return True
		print("Block not added")
		print(f"block.previous_hash = {block.previous_hash}")
		print(f"self.last_block.hash() = {self.last_block().hash()}")
		return False

	def consensus(self):
		longest_chain = self.blocks
		wallets = self.get_wallets()
		nodes = self.get_nodes()
		difficulty = self.get_difficulty()
		fee = self.get_fee()
		for node in list(self.nodes):
			try:
				r = requests.get(f"{node}")
				json = r.json()
				blocks = self.blocks_from_json(json["blocks"])
			except Exception as e:
				print(str(e))
			else:
				if len(blocks) >= len(longest_chain) and self.timestamp_genesis(blocks) <= self.timestamp_genesis() and self.validate(blocks):
					longest_chain = blocks
					wallets = json["wallets"]
					nodes = json["nodes"]
					difficulty = json["difficulty"]
					fee = json["fee"]
		self.blocks = longest_chain
		self.wallets = self.wallets_from_json(wallets)
		self.add_nodes(nodes)
		self.set_difficulty(difficulty)
		self.set_fee(fee)

	def announce_block(self, block):
		for node in self.nodes:
			try:
				r = requests.post(f"{node}blocks/add", json={"block":{block.index:block.__dict__}})
			except:
				pass
	
	def announce_nodes(self, nodes):
		for node in self.nodes:
			try:
				r = requests.post(f"{node}nodes/add", json={"nodes":nodes})
			except:
				pass

	def announce_wallet(self, wallet):
		for node in self.nodes:
			try:
				r = requests.post(f"{node}wallets/add", json={"wallet":self.get_wallet(wallet.address)})
			except:
				pass
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
import secrets
import urllib3
from .Wallet import Wallet

http = urllib3.PoolManager()

class Blockchain:
	def __init__(self):
		self.unconfirmed_transactions = []
		self.blocks = []
		self.wallets = {}
		self.nodes = set()
		self.difficulty = 4
		self.fee = Decimal("0.01")
		self.reward = Decimal("100.00")
		self.vault, self.private_key = self.new_wallet()
		self.create_genesis()

	def create_genesis(self):
		block = Block(0, "0"*64)
		amount = Decimal("1000.00")
		transaction = {
			"txid":"",
			"timestamp":str(datetime.datetime.utcnow()),
			"sender":f"0x{'0'*32}",
			"recipient":self.vault.address,
			"amount":str(amount),
			"fee":str(Decimal(self.get_fee()) * amount),
			"signature":""
		}
		transaction["txid"] = sha256_hash(json.dumps(transaction))
		block.data = transaction
		mined = False
		while not mined:
			nonce = int("".join([str(secrets.randbelow(10)) for i in range(8)]))
			block.nonce = nonce
			block.reward = str(self.reward / Decimal("2")**(Decimal(str(block.index)) // Decimal("100")))
			new_hash = block.hash()
			if new_hash.startswith("0"*self.get_difficulty()):
				mined = True
				block.miner = self.vault.address
				self.blocks.append(block)
	
	def timestamp_genesis(self, blocks=None):
		if blocks is None:
			blocks = self.blocks
		return datetime.datetime.fromisoformat(blocks[0].data["timestamp"])	

	def new_wallet(self):
		unique = False
		while not unique:
			wallet = Wallet()
			private_key = wallet.generate_keys()
			unique = wallet.address not in self.wallets
		self.wallets[wallet.address] = wallet
		self.announce_wallet(wallet)
		return (wallet, private_key)

	def add_wallet(self, data):
		if data["address"] not in self.wallets.keys():
			wallet = Wallet(data["public_key"])
			self.wallets[data["address"]] = wallet
			return True
		return False

	def parse_wallet(self, wallet):
		try:
			wallet = dict(wallet.__dict__)
			wallet["balance"] = str(self.get_balance(wallet["address"]))
		except:
			return False
		return wallet

	def get_wallets(self):
		wallets = [self.parse_wallet(wallet) for (address, wallet) in self.wallets.items()]
		return wallets

	def get_wallet(self, address):
		if address in self.wallets.keys():
			return self.wallets[address]
		return False

	def get_balance(self, address, include_unconfirmed=False):
		if address not in self.wallets.keys():
			return False
		balance = Decimal("0")
		for block in self.blocks:
			data = block.data
			if block.miner == address:
				balance += Decimal(data["fee"]) + Decimal(block.reward)
			if data["sender"] == address:
				balance -= Decimal(data["amount"]) + Decimal(data["fee"])
			if data["recipient"] == address:
				balance += Decimal(data["amount"])
		if include_unconfirmed:
			for unconfirmed in self.unconfirmed_transactions:
				if unconfirmed["sender"] == address:
					balance -= Decimal(unconfirmed["amount"]) + Decimal(unconfirmed["fee"])
				if unconfirmed["recipient"] == address:
					balance += Decimal(unconfirmed["amount"])
		return balance

	def parse_block(self, block):
		try:
			parsed = dict(block.__dict__)
			parsed["hash"] = block.hash()
		except:
			return False
		return parsed

	def get_blocks(self):
		blockchain = {block.index:self.parse_block(block) for block in self.blocks}
		return blockchain

	def get_block(self, index):
		if 0 <= index < len(self.blocks):
			return self.parse_block(self.blocks[index])
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

	def get_reward(self):
		return str(self.reward)

	def set_reward(self, reward):
		try:
			self.reward = Decimal(str(reward))
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

	def get_transaction(self, txid):
		for block in self.blocks:
			if block.data["txid"] == txid:
				return block.data
		return False

	def get_unconfirmed_transactions(self, address=None):
		unconfirmed_transactions = []
		for transaction in self.unconfirmed_transactions:
			if (transaction["sender"] == address or transaction["recipient"] == address) or not address:
				unconfirmed_transactions.append(transaction)
		return unconfirmed_transactions

	def get_unconfirmed_transaction(self, txid):
		for transaction in self.unconfirmed_transactions:
			if transaction["txid"] == txid:
				return transaction
		return False

	def check_unique_signature(self, signature):
		for block in self.blocks:
			transaction = block.data
			if transaction["signature"] == signature:
				return False
		for transaction in self.unconfirmed_transactions:
			if transaction["signature"] == signature:
				return False
		return True

	def validate_transaction(self, sender, recipient, amount, signature):
		sender = self.get_wallet(sender)
		recipient = self.get_wallet(recipient)
		try:
			assert sender
			assert recipient
			amount = Decimal(str(amount))
			assert amount > Decimal("0")
			signature = signature[:-64]
		except:
			return False
		else:
			insufficient_balance = self.get_balance(sender.address, include_unconfirmed=True) - (amount + amount * self.fee) < Decimal('0')
			message = ":".join([sender.address, recipient.address, str(amount)])
			verified = Wallet.verify(sender.public_key, message, signature)
			if not insufficient_balance and verified:
				return True
		return False

	def new_transaction(self, sender, recipient, amount, signature):
		amount = Decimal(str(amount))
		if self.validate_transaction(sender, recipient, amount, signature) and self.check_unique_signature(signature):
			transaction = {
				"txid":"",
				"timestamp":str(datetime.datetime.utcnow()),
				"sender":sender,
				"recipient":recipient,
				"amount":str(amount),
				"fee":str(amount * self.fee),
				"signature":signature
			}
			transaction["txid"] = sha256_hash(json.dumps(transaction))
			self.unconfirmed_transactions.append(transaction)
			self.announce_transaction(transaction)
			return transaction
		return False

	def add_transaction(self, transaction):
		sender = transaction["sender"]
		recipient = transaction["recipient"]
		amount = transaction["amount"]
		signature = transaction["signature"]
		if self.validate_transaction(sender, recipient, amount, signature) and self.check_unique_signature(signature):
			self.unconfirmed_transactions.append(transaction)
			return True
		return False
	
	def mine(self):
		confirmed = []
		while self.unconfirmed_transactions:
			transaction = self.unconfirmed_transactions.pop(0)
			last_block = self.last_block()
			last_hash = last_block.hash()
			block = Block(last_block.index + 1, last_hash)
			block.data = transaction
			mined = False
			while not mined:
				nonce = int("".join([str(secrets.randbelow(10)) for i in range(8)]))
				block.nonce = nonce
				block.reward = str(self.reward / Decimal("2")**(Decimal(str(block.index)) // Decimal("100")))
				new_hash = block.hash()
				if new_hash.startswith("0"*self.get_difficulty()):
					mined = True		
			blocks_before = self.get_blocks()
			self.consensus()
			if blocks_before == self.get_blocks():
				block.miner = str(self.vault)
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
			transaction = block.data
			if i > 0:
				valid_signature = self.validate_transaction(transaction["sender"], transaction["recipient"], transaction["amount"], transaction["signature"])
			else:
				valid_signature = True
			if (block.previous_hash != previous_hash) or (not valid_signature):
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
			b.miner = block["miner"]
			b.reward = block["reward"]
			blocks.append(b)
		return blocks

	def import_blocks(self, blocks):
		self.blocks = self.blocks_from_json(blocks)
		return True		

	def wallets_from_json(self, wallets):
		new_wallets = {}
		for data in wallets:
			wallet = Wallet(data["public_key"])
			new_wallets[data["address"]] = wallet
		return new_wallets

	def import_wallets(self, wallets):
		self.wallets = self.wallets_from_json(wallets)
		return True

	def add_block(self, block):
		if block.data in self.unconfirmed_transactions:
			self.unconfirmed_transactions.remove(block.data)
		if block.index == 0 and datetime.datetime.fromisoformat(block["data"]["timestamp"]) < datetime.datetime.fromisoformat(self.blocks[0].data["timestamp"]):
			self.blocks = [block]
			return True
		elif block.previous_hash == self.last_block().hash():
			self.blocks.append(block)
			return True
		return False

	def consensus(self):
		longest_chain = self.blocks
		unconfirmed = self.get_unconfirmed_transactions()
		wallets = self.get_wallets()
		nodes = self.nodes
		difficulty = self.get_difficulty()
		fee = self.get_fee()
		reward = self.get_reward()
		for node in list(self.nodes):
			try:
				r = http.request("GET", f"{node}nodes/add")
				data = json.loads(r.data.decode())
				blocks = self.blocks_from_json(data["blocks"])
			except Exception as e:
				print(str(e))
			else:
				if len(blocks) >= len(longest_chain) and self.timestamp_genesis(blocks) <= self.timestamp_genesis() and self.validate(blocks):
					longest_chain = blocks
					unconfirmed = data["unconfirmed"]
					wallets = data["wallets"]
					nodes = data["nodes"]
					difficulty = data["difficulty"]
					fee = data["fee"]
					reward = data["reward"]
		self.blocks = longest_chain
		self.import_wallets(wallets)
		self.unconfirmed_transactions = unconfirmed
		self.add_nodes(nodes)
		self.set_difficulty(difficulty)
		self.set_fee(fee)
		self.set_reward(reward)

	def announce_block(self, block):
		for node in self.nodes:
			try:
				r = http.request("POST", f"{node}blocks/add", headers={"Content-Type":"application/json"}, body=json.dumps({"block":{block.index:block.__dict__}}))
			except:
				pass
	
	def announce_nodes(self, nodes):
		for node in self.nodes:
			try:
				r = http.request("POST", f"{node}nodes/add", headers={"Content-Type":"application/json"}, body=json.dumps({"nodes":nodes}))
			except:
				pass

	def announce_wallet(self, wallet):
		for node in self.nodes:
			try:
				r = http.request("POST", f"{node}wallets/add", headers={"Content-Type":"application/json"}, body=json.dumps({"wallet":self.parse_wallet(wallet)}))
			except:
				pass

	def announce_transaction(self, transaction):
		for node in self.nodes:
			try:
				r = http.request("POST", f"{node}transactions/add", headers={"Content-Type":"application/json"}, body=json.dumps({"transaction":transaction}))
			except:
				pass
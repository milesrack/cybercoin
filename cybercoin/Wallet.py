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
from Crypto.PublicKey import RSA
from Crypto.Signature import PKCS1_v1_5
from Crypto.Hash import SHA256
from .Cryptography import sha256_hash
import base64

class Wallet:
	def __init__(self, public_key=None):
		self.address = ""
		self.public_key = ""
		if public_key is None:
			self.generate_keys()
		else:
			self.import_key(public_key)

	def __str__(self):
		return self.address
	
	@staticmethod
	def key_from_base64(key):
		return RSA.import_key(base64.b64decode(bytes(key, "utf-8")))
	
	@staticmethod
	def key_to_base64(key):
		return base64.b64encode(key.exportKey()).decode()

	def import_key(self, public_key):
		public_key = Wallet.key_from_base64(public_key)
		modulus_hash = sha256_hash(public_key.n)		
		upper = modulus_hash[:32]
		lower = modulus_hash[32:]
		self.address = "0x" + "".join([hex(int(upper[i],16) ^ int(lower[i],16))[2:] for i in range(32)])
		self.public_key = Wallet.key_to_base64(public_key)

	def generate_keys(self):
		key = RSA.generate(2048)
		public_key = key.publickey()
		self.import_key(Wallet.key_to_base64(public_key))
		return Wallet.key_to_base64(key)

	@staticmethod
	def sign(private_key, message):
		private_key = key_from_base64(private_key)
		signer = PKCS1_v1_5.new(private_key)
		digest = SHA256.new()
		digest.update(bytes(message, "utf-8"))
		return signer.sign(digest).hex()

	@staticmethod
	def verify(public_key, message, signature):
		public_key = key_from_base64(public_key)
		signer = PKCS1_v1_5.new(public_key)
		digest = SHA256.new()
		digest.update(bytes(message, "utf-8"))
		return signer.verify(digest, bytes(bytearray.fromhex(signature)))
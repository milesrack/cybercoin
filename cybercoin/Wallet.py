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
from Crypto.PublicKey import ECC
from Crypto.Signature import DSS
from Crypto.Hash import SHA256
import base64

class Wallet:
	def __init__(self, key=None):
		self.address = ""
		self.public_key = ""
		if key is None:
			self.generate_keys()
		else:
			self.import_key(key)

	def __str__(self):
		return self.address
	
	@staticmethod
	def key_from_base64(key):
		der = base64.b64decode(bytes(key, "utf-8"))
		return ECC.import_key(der)
	
	@staticmethod
	def key_to_base64(key):
		der = key.export_key(format="DER")
		return base64.b64encode(der).decode()

	def import_key(self, public_key):
		public_key = Wallet.key_from_base64(public_key).public_key()
		key_hash = SHA256.new(public_key.export_key(format="DER")).hexdigest()
		upper = key_hash[:32]
		lower = key_hash[32:]
		self.address = "0x" + "".join([hex(int(upper[i],16) ^ int(lower[i],16))[2:] for i in range(32)])
		self.public_key = Wallet.key_to_base64(public_key)

	def generate_keys(self):
		key = ECC.generate(curve="p521")
		public_key = key.public_key()
		self.import_key(Wallet.key_to_base64(public_key))
		return Wallet.key_to_base64(key)

	@staticmethod
	def sign(private_key, message):
		private_key = Wallet.key_from_base64(private_key)
		signer = DSS.new(private_key, "fips-186-3")
		digest = SHA256.new(bytes(message, "utf-8"))
		return signer.sign(digest).hex()

	@staticmethod
	def verify(public_key, message, signature):
		public_key = Wallet.key_from_base64(public_key)
		verifier = DSS.new(public_key, "fips-186-3")
		digest = SHA256.new(bytes(message, "utf-8"))
		try:
			verifier.verify(digest, bytes(bytearray.fromhex(signature)))
		except:
			return False
		return True

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
import random
import datetime
from .Cryptography import sha256_hash

class Wallet:
	def __init__(self):
		self.address = ""
		# TODO: private key stuff
		self.generate_address()

	def __str__(self):
		return self.address
	
	def generate_address(self):
		random_hash = sha256_hash("".join([str(random.randint(0,9)) for i in range(8)]) + str(datetime.datetime.now()))
		upper = random_hash[:32]
		lower = random_hash[32:]
		self.address = "0x" + "".join([hex(int(upper[i],16) ^ int(lower[i],16))[2:] for i in range(32)])
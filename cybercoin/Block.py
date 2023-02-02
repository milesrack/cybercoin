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
import json
from .Cryptography import sha256_hash

class Block:
	def __init__(self, index=0, previous_hash="0"*64):
		self.index = index
		self.previous_hash = previous_hash
		self.nonce = 0
		self.data = {}

	def hash(self):
		return sha256_hash(json.dumps(self.__dict__, sort_keys=True))

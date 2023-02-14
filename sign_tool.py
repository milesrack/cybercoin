#!/usr/bin/env python3
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
from cybercoin import Wallet
from cybercoin import sha256_hash
import datetime

private_key = input("Private key: ")
signer = Wallet(private_key)
print(f"Sender: {signer.address}")
recipient = input("Recipient: ")
amount = input("Amount: ")
message = ":".join([signer.address, recipient, amount])
signature = Wallet.sign(private_key, message) + sha256_hash(datetime.datetime.utcnow())
print(f'{{"sender":"{signer.address}", "recipient":"{recipient}", "amount":"{amount}", "signature":"{signature}"}}')
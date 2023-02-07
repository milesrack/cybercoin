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
import secrets
import math
import base64

def is_prime(x):
	if x == 0 or x == 1:
		return False
	for i in range(2, x):
		if x % i == 0:
			return False
	return True

def get_primes(min=1000, max=65536):
	primes = []
	[primes.append(i) if is_prime(i) else 0 for i in range(min, max)]
	return primes

def factor(x):
	factors = []
	for i in range(2,x):
		if x % i == 0:
			factors.append(i)
	return factors

def phi(p, q):
	return (p-1)*(q-1)

def possible_e(n, phi):
	keys = []
	for i in range(2,phi):
		if math.gcd(i,n) == 1 and math.gcd(i,phi) == 1:
			keys.append(i)
	return keys

def possible_d(e, phi):
	keys = []
	i = phi + 1
	#while len(keys) < 100:
	while not keys:
		if i*e % phi == 1:
			keys.append(i)
		i += 1
	return keys

def string_to_hex(string):
	return ''.join([hex(char)[2:] for char in bytes(string, "utf-8")])

def hex_to_string(hex):
	return ''.join([chr(int(hex[i:i+2],16)) for i in range(0,len(hex),2)])

def encrypt(pt, e, n):
	ct = []
	for char in pt:
		ct.append(char**e % n)
	return ct
	#return "".join(["{:08x}".format(c**e % n) for c in pt.encode()])

def decrypt(ct, d, n):
	pt = []
	for char in ct:
		pt.append(char**d % n)
	return pt
	#ct = f"{ct:0{padding}x}"
	#return "".join([chr(int(ct[i:i+8],16)**d % n) for i in range(0,len(ct),8)])

primes = get_primes(min=0,max=1000)
primes.remove(2)

p = secrets.choice(primes)
primes.remove(p)
print(f"p = {p}")

q = secrets.choice(primes)
primes.remove(q)
print(f"q = {q}")

n = p*q
print(f"n = {n}")

phi = phi(p,q)
print(f"phi = {phi}")

e = secrets.choice(possible_e(n,phi))
#e = 65537
print(f"e = {e}")

d = secrets.choice(possible_d(e,phi))
print(f"d = {d}")

public_key = (e, n)
print(f"public_key = {public_key}")

private_key = (d, n)
print(f"private_key = {private_key}")

pt = "hello world"
print(f"pt = {pt}")

ct = encrypt(pt.encode(), e, n)
#padding = len(ct)
#ct = int(ct,16)
print(f"ct = {ct}")

decrypted = decrypt(ct, d, n)
print(f"decrypted = {decrypted}")
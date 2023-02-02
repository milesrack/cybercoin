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
from flask import Flask, request
import requests
from cybercoin import Blockchain as Cybercoin

app = Flask(__name__)

cyb = Cybercoin()

vault = cyb.vault()
alice = cyb.new_wallet()
bob = cyb.new_wallet()
cyb.new_transaction(vault, alice, 2000)
cyb.mine()

@app.route("/")
def home():
	return {"blocks":cyb.get_blocks(), "wallets":cyb.get_wallets(), "nodes":list(cyb.get_nodes()), "difficulty":cyb.get_difficulty(), "fee":cyb.get_fee()}

@app.route("/wallets")
def wallets():
	return {"wallets":cyb.get_wallets()}

@app.route("/wallets/new")
def new_wallet():
	return {"wallet":cyb.get_wallet(cyb.new_wallet().address)}

@app.route("/wallets/<wallet>")
def wallet(wallet):
	return {"wallet":cyb.get_wallet(wallet)}

@app.route("/length")
def length():
	return {"length":cyb.length()}

@app.route("/blocks")
def blocks():
	return {"blocks":cyb.get_blocks()}

@app.route("/blocks/add", methods=["POST"])
def add_block():
	json = request.get_json()
	print(json)
	new_block = cyb.blocks_from_json(json["block"])[0]
	return {"added":cyb.add_block(new_block)}

@app.route("/blocks/<int:block>")
def block(block):
	return {"block":cyb.get_block(block)}

@app.route("/difficulty", methods=["GET","POST"])
def difficulty():
	if request.method == "POST":
		try:
			req = request.get_json()
			difficulty = req["difficulty"]
		except:
			pass
		else:
			cyb.set_difficulty(difficulty)
	return {"difficulty":cyb.get_difficulty()}

@app.route("/fee", methods=["GET", "POST"])
def fee():
	if request.method == "POST":
		try:
			req = request.get_json()
			fee = req["fee"]
		except:
			pass
		else:
			cyb.set_fee(fee)
	return {"fee":cyb.get_fee()}

@app.route("/transactions")
def transactions():
	return {"transactions":cyb.get_transactions()}

@app.route("/transactions/pending")
def pending_transactions():
	return {"transactions":cyb.get_pending()}

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
	transaction = {}
	if request.method == "POST":
		try:
			req = request.get_json()
			sender = cyb.wallet(req["sender"])
			recipient = cyb.wallet(req["recipient"])
			amount = req["amount"]
		except:
			pass
		else:
			transaction = cyb.new_transaction(sender, recipient, amount)
	return {"transaction":transaction}

@app.route("/transactions/wallet/<wallet>")
def wallet_transactions(wallet):
	return {"transaction":cyb.get_transactions(wallet)}

@app.route("/transactions/<transaction>")
def transaction(transaction):
	return {"transaction":cyb.get_transaction(transaction)}

@app.route("/mine")
def mine():
	return {"transactions":cyb.mine()}

@app.route("/validate")
def validate():
	return {"valid":cyb.validate()}

@app.route("/nodes")
def nodes():
	return {"nodes":list(cyb.get_nodes())}

@app.route("/nodes/add", methods=["POST"])
def add_nodes():
	try:
		new_node = request.get_json()["node"]
		#r = requests.get(f"{node}validate")
		#assert r.json()["valid"] == "true"
	except:
		pass
	else:
		cyb.add_nodes([new_node])
	return {"blocks":cyb.get_blocks(), "wallets":cyb.get_wallets(), "nodes":list(cyb.get_nodes()), "difficulty":cyb.get_difficulty(), "fee":cyb.get_fee()}

@app.route("/nodes/register", methods=["POST"])
def register_node():
	try:
		remote_node = request.get_json()["node"]
		new_node = request.host_url
		r = requests.post(f"{remote_node}nodes/add", json={"node":new_node})
		json = r.json()
	except:
		pass
	else:
		blocks = cyb.blocks_from_json(json["blocks"])
		if cyb.validate(blocks) and len(blocks) > cyb.length():
			cyb.blocks = blocks
			cyb.wallets = cyb.wallets_from_json(json["wallets"])
			cyb.add_nodes(json["nodes"])
			cyb.set_difficulty(json["difficulty"])
			cyb.set_fee(json["fee"])
			#print("returned remote node")
			return json
	#print("returned local data")
	return {"blocks":cyb.get_blocks(), "wallets":cyb.get_wallets(), "nodes":list(cyb.get_nodes()), "difficulty":cyb.get_difficulty(), "fee":cyb.get_fee()}

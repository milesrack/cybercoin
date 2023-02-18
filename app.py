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
from cybercoin import Blockchain
import urllib3
import json
import re

def parse_url(url):
	if not re.match(r"^https?://", url):
		url = "http://" + url
	if not re.match(r".*/$", url):
		url += "/"
	return url

def load_config():
	try:
		with open("config.json", "r") as f:
			data = json.loads(f.read())
			return (parse_url(data["registration_node"]), data["private_key"])
	except:
		return (None, None)

app = Flask(__name__)
http = urllib3.PoolManager()
registration_node, private_key = load_config()
cyb = Blockchain(private_key=private_key)

@app.route("/")
def home():
	return {}

@app.route("/wallets")
def wallets():
	return {"wallets":cyb.get_wallets()}

@app.route("/wallets/new")
def new_wallet():
	wallet, private_key = cyb.new_wallet()
	wallet_ = cyb.parse_wallet(wallet)
	wallet_["private_key"] = private_key
	return {"wallet":wallet_}

@app.route("/wallets/add", methods=["POST"])
def add_wallet():
	try:
		data = request.get_json()
		wallet = data["wallet"]
	except:
		return {"added":False}
	else:
		return {"added":cyb.add_wallet(wallet)}

@app.route("/wallets/<address>")
def wallet(address):
	return {"wallet":cyb.parse_wallet(cyb.get_wallet(address))}

@app.route("/length")
def length():
	return {"length":len(cyb.blocks)}

@app.route("/blocks")
def blocks():
	return {"blocks":cyb.get_blocks()}

@app.route("/blocks/add", methods=["POST"])
def add_block():
	try:
		data = request.get_json()
		new_block = cyb.blocks_from_json(data["block"])[0]
	except:
		return {"added":False}
	else:
		return {"added":cyb.add_block(new_block)}

@app.route("/blocks/last")
def last_block():
	return {"block":cyb.get_block(cyb.last_block().index)}

@app.route("/blocks/<int:index>")
def block(index):
	return {"block":cyb.get_block(index)}

@app.route("/difficulty")
def difficulty():
	return {"difficulty":cyb.get_difficulty()}

@app.route("/fee")
def fee():
	return {"fee":cyb.get_fee()}

@app.route("/reward")
def reward():
	return {"reward":cyb.get_reward()}

@app.route("/transactions")
def transactions():
	return {"transactions":cyb.get_transactions()}

@app.route("/transactions/unconfirmed")
def unconfirmed_transactions():
	return {"transactions":cyb.get_unconfirmed_transactions()}

@app.route("/transactions/unconfirmed/<txid>")
def unconfirmed_transaction(txid):
	return {"transaction":cyb.get_unconfirmed_transaction(txid)}

@app.route("/transactions/unconfirmed/wallet/<address>/")
def unconfirmed_transactions_wallet(address):
	return {"transactions":cyb.get_unconfirmed_transactions(address)}

@app.route("/transactions/new", methods=["POST"])
def new_transaction():
	transaction = False
	try:
		data = request.get_json()
		sender = data["sender"]
		recipient = data["recipient"]
		amount = data["amount"]
		signature = data["signature"]
	except:
		pass
	else:
		transaction = cyb.new_transaction(sender, recipient, amount, signature)
	return {"transaction":transaction}

@app.route("/transactions/add", methods=["POST"])
def add_transaction():
	try:
		data = request.get_json()
		transaction = data["transaction"]
	except:
		return {"added":False}
	else:
		return {"added":cyb.add_transaction(transaction)}

@app.route("/transactions/wallet/<address>")
def wallet_transactions(address):
	return {"transactions":cyb.get_transactions(address)}

@app.route("/transactions/<txid>")
def transaction(txid):
	return {"transaction":cyb.get_transaction(txid)}

@app.route("/mine")
def mine():
	return {"transactions":cyb.mine()}

@app.route("/validate")
def validate():
	return {"valid":cyb.validate()}

@app.route("/nodes")
def nodes():
	return {"nodes":list(cyb.get_nodes())}

@app.route("/nodes/add", methods=["GET","POST"])
def add_nodes():
	if request.method == "POST":
		try:
			nodes = request.get_json()["nodes"]
		except:
			pass
		else:
			cyb.add_nodes(nodes)
	return {"blocks":cyb.get_blocks(), "unconfirmed":cyb.get_unconfirmed_transactions(), "wallets":cyb.get_wallets(), "nodes":list(cyb.get_nodes()), "difficulty":cyb.get_difficulty(), "fee":cyb.get_fee(), "reward":cyb.get_reward()}

@app.route("/nodes/register", methods=["POST"])
def register_nodes():
	try:
		registration_node = request.get_json()["node"]
		if registration_node != "":
			cyb.add_nodes([registration_node, request.host_url])
			r = http.request("POST", f"{registration_node}nodes/add", headers={"Content-Type":"application/json"}, body=json.dumps({"nodes":list(cyb.get_nodes())}))
			data = json.loads(r.data.decode())
			cyb.import_blocks(data["blocks"])
			cyb.unconfirmed_transactions = data["unconfirmed"]
			cyb.import_wallets(data["wallets"])
			cyb.add_nodes(data["nodes"])
			cyb.set_difficulty(data["difficulty"])
			cyb.set_fee(data["fee"])
			cyb.set_reward(data["reward"])
			cyb.announce_nodes(list(cyb.get_nodes()))
			cyb.announce_wallet(cyb.vault)
	except Exception as e:
		print(e)
		return {"registered":False}
	else:
		return {"registered":True}

with open(f"keys/{cyb.vault.address}.key", "w") as f:
	f.write(cyb.private_key)
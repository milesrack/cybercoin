from cybercoin import Wallet
import requests

private_key = input("Private key: ")
signer = Wallet(private_key)
print(signer.__dict__)
recipient = input("Recipient: ")
amount = input("Amount: ")
last_hash = requests.get("http://127.0.0.1:5000/blocks/last").json()["block"]["hash"]
message = ":".join([signer.address, recipient, amount, last_hash])
print(Wallet.sign(private_key, message))
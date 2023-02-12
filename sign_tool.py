from cybercoin import Wallet

private_key = input("Private key: ")
signer = Wallet(private_key)
print(f"Sender: {signer.address}")
recipient = input("Recipient: ")
amount = input("Amount: ")
message = ":".join([signer.address, recipient, amount])
print(f"Signature: {Wallet.sign(private_key, message)}")
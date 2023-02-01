# Cybercoin
A blockchain implementation for the "Cybercoin" (CYB) cryptocurrency at CBCYBER.

## Installation
```
git clone https://github.com/milesrack/cybercoin
cd cybercoin
python3 setup.py install
```

## Usage
### Cybercoin Package
```python
from cybercoin import Blockchain as Cybercoin

cyb = Cybercoin()
# Creates a new blockchain instances

alice = cyb.new_wallet()
# Creates a new wallet object
bob = cyb.new_wallet()
# Creates a new wallet object
vault = cyb.vault()
# Creates a new "vault" wallet object with a balance of Infinity

wallets = cyb.get_wallets()
print(wallets)
# Returns a dictionary of all wallet addresses and balances

wallet = cyb.get_wallet("0x00000000000000000000000000000000")
print(wallet)
# Takes a wallet address as the argument
# Returns a dictionary of the wallet addresses and balance

length = cyb.length()
print(length)
# Returns the length of the blockchain

blockchain = cyb.get_blocks()
print(blockchain)
# Returns a dictionary of the index of each block and the block information

block = cyb.get_block(0)
print(block)
# Takes the index of a block as the argument
# Returns a dictionary of the block information

difficulty = cyb.get_difficulty()
print(difficulty)
# Returns the mining difficulty

cyb.set_difficulty(5)
# Takes an integer between 0 and 63 as the argument and sets the mining difficulty
# Returns True if successful or False if unsuccessful

fee = cyb.get_fee()
print(fee)
# Returns the blockchain transaction fee

cyb.set_fee(0.01)
# Takes the decimal representation of the new blockchain transaction fee as an argument
# ex. 0.01 would set the fee to 1%
# Returns True if successful or False if unsuccessful

transactions = cyb.get_transactions()
transactions = cyb.get_transactions("0x00000000000000000000000000000000")
print(transactions)
# Takes an optional arugment of the wallet address to search
# Returns a dictionary of all transaction data from each block
# If a wallet address is specified only transactions sent to or from that wallet are returned

transaction = cyb.get_transaction("ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff")
print(transaction)
# Takes the transaction ID (txid) of a transaction as the argument
# Returns a dictionary of the transaction data if found or False if not found

new_transaction = cyb.new_transaction(vault, alice, 100.00)
print(new_transaction)
# Takes the wallet object of the sender as the first argument, recipient as the second argument, and amount as the third argument
# ex. This example would send 100.00 CYB from vault to alice
# Returns a dictionary of the transaction data if successful or False if unsuccessful

confirmed_transactions = cyb.mine()
print(confirmed_transactions)
# Mines a new block for each unconfirmed transaction
# Returns a dictionary list of all newly mined blocks

valid = cyb.validate()
print(valid)
# Validates the hashes of each block to ensure its integrity
# Takes an optional argument of a list of Block() objects to validate
# Returns True if all blocks are valid and False if a block was tampered with
```
### Cybercoin API
#### Wallets
#### Blocks
#### Difficulty
#### Fee
#### Transactions
#### Mine

## TODO
- [x] Built API for cybercoin
- [ ] Allow registration of new nodes
- [ ] Write consensus algorithm
- [ ] Build front-end application

## License
Licensed under the [GNU General Public License Version 3.0](https://www.gnu.org/licenses/gpl-3.0.txt)

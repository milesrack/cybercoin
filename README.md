# Cybercoin :computer:
A blockchain implementation for the Cybercoin (CYB) cryptocurrency at CB CYBER.

## :pushpin: Installation
```
git clone https://github.com/milesrack/cybercoin
cd cybercoin
python3 setup.py install
```

## :pushpin: Getting Started

## :pushpin: Documentation
- [Python Package](docs/package.md)
- [API Endpoints](docs/api.md)

## :pushpin: TODO
- [x] Built API for cybercoin
- [x] Allow registration of new nodes
- [x] Register current node with new remote nodes
- [x] Write consensus algorithm
- [x] Calculate wallet balance from blocks
- [x] Private keys to prevent forging transactions
- [x] Pay network fees
- [x] Import/export keys
- [x] Return wallets as list in API
- [x] Transaction signing and verification
- [x] Change from RSA + PKCS to ECC + DSS
- [x] Regenerate duplicate vault address on node registration
- [x] verify_transaction() function for less code reuse
- [x] Prevent signature replay
- [x] Replace requests bloat with urllib3
- [ ] Auto register and import vault on start
- [ ] Build front-end application

## :pushpin: License
Licensed under the [GNU General Public License Version 3.0](https://www.gnu.org/licenses/gpl-3.0.txt)

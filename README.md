# Cybercoin :computer:
A blockchain implementation for the Cybercoin (CYB) cryptocurrency at CB CYBER.

## :pushpin: Requirements
- docker

## :pushpin: Installation
```bash
git clone https://github.com/milesrack/cybercoin
cd cybercoin
```

## :pushpin: Getting Started
### Building the Image
```bash
docker build -t cybercoin:latest .
```

### Running the Container
```bash
docker run --rm -v $(pwd):/opt/cybercoin -p 8000:8000 -d cybercoin:latest
```

### Wallet Keys
Private keys for your cybercoin wallet are stored in a shared volume under the `keys/` folder.

### Logs
The `access.log` and `error.log` files are stored in a shared volume under the `logs/` folder.

### Editing the Configuration
```bash
$ cat config.py
```
```python
registration_node = "http://127.0.0.1:8000/"
private_key = ""

port = "8000"
bind = "0.0.0.0:" + port
wsgi_app = "app:app"
accesslog = "logs/access.log"
errorlog = "logs/error.log"
pidfile = "/tmp/gunicorn.pid"
worker_class = "gevent"
daemon = True
```

`registration_node`: The API endpoint of a valid cybercoin node to sync with. By default this is localhost.

`private_key`: The private key of a wallet you wish to import. This wallet will recieve transaction fees and block rewards for blocks that the node mines. If you leave this value blank a new wallet will be created.

### `manage.sh`
The `manage.sh` file is used to start, stop, and clean files for the cybercoin node. This may be useful if you want to debug issues or change settings inside the container.

First find the `CONTAINER ID` of the running cybercoin node:
```
docker ps
```

Then open an interactive shell inside the container:
```
docker exec -it <CONTAINER ID> /bin/sh
```

To stop the cybercoin node:
```
./manage.sh stop
```

To start the cybercoin node:
```
./manage.sh start
```

To clean files (logs, private keys, and cached files):
```
./manage.sh clean
```

## :pushpin: API Endpoints
### `/`

### `/wallets`

### `/wallets/new`

### `/wallets/<address>`

### `/length`

### `/blocks`

### `/blocks/last`

### `/blocks/<index>`

### `/difficulty`

### `/fee`

### `/reward`

### `/transactions`

### `/transactions/unconfirmed`

### `/transactions/unconfirmed/<txid>`

### `/transactions/unconfirmed/wallet/<address>/`

### `/transactions/wallet/<address>`

### `/transactions/<txid>`

### `/mine`

### `/validate`

### `/nodes`

## :pushpin: License
Licensed under the [GNU General Public License Version 3.0](https://www.gnu.org/licenses/gpl-3.0.txt)

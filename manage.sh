#!/bin/sh
cd $(dirname $0)
if [[ $1 == "start" ]]
then
	mkdir -p keys logs
	rm -f /tmp/gunicorn.pid
	gunicorn --config config.py
	REGISTERED=false; while ! $REGISTERED; do curl -s -X POST "http://127.0.0.1:$(python3 -c "import config; print(config.port)")/nodes/register" -H "Content-Type: application/json" --data '{"node":"'"$(python3 -c "import config; print(config.registration_node)")"'"}' > /dev/null && REGISTERED=true; done
	# for key in $(ls keys/); do echo -e "ADDRESS: $key\nPRIVATE KEY: $(cat keys/$key)\n"; done
	tail -f logs/access.log
elif [[ $1 == "stop" ]]
then
	kill $(cat /tmp/gunicorn.pid)
elif [[ $1 == "clean" ]]
then
	rm -rf keys/ logs/ __pycache__/ cybercoin/__pycache__/ build/ cybercoin.egg-info/ dist/ /tmp/gunicorn.pid
else
	echo "Usage: $0 ( start | stop | clean )"
fi

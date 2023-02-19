#!/bin/sh
PORT=8000
cd $(dirname $0)
if [[ $1 == "start" ]]
then
	#if [[ $1 ]]
	#then
	#	PORT=$1
	#else
	#	CURRENT_PORT=$(($(ls proc/*.proc 2>/dev/null | grep -oE "[0-9]+" | sort -r | head -n 1)))
	#	if [ $CURRENT_PORT -gt 0 ]
	#	then
	#		PORT=$(($CURRENT_PORT+1))
	#	else
	#		PORT=8000
	#	fi
	#fi
	mkdir -p keys logs proc
	gunicorn app:app -b 0.0.0.0:$PORT --access-logfile logs/access.log --error-logfile logs/error.log -p proc/$PORT.proc --worker-class gevent -D
	REGISTERED=false; while ! $REGISTERED; do curl -s -X POST "http://127.0.0.1:$PORT/nodes/register" -H "Content-Type: application/json" --data '{"node":"'"$(cat config.json | jq .registration_node -r)"'"}' && REGISTERED=true; done
	tail -f logs/access.log
elif [[ $1 == "stop" ]]
then
	for proc in $(find proc/ -name "*.proc"); do kill $(cat $proc); done
elif [[ $1 == "clean" ]]
then
	rm -rf keys/ logs/ proc/ __pycache__/ cybercoin/__pycache__/ build/ cybercoin.egg-info/ dist/
else
	echo "Usage: $0 ( start | stop | clean )"
fi

#!/bin/sh
if [ $1 ]
then
	PORT=$1
else
	CURRENT_PORT=$(($(ls *.proc 2>/dev/null | sed -E 's/([0-9]+).proc/\1/g' | sort -r | head -n 1)))
	if [ $CURRENT_PORT -gt 0 ]
	then
		PORT=$(($CURRENT_PORT+1))
	else
		PORT=8000
	fi
fi
gunicorn app:app -b 0.0.0.0:$PORT --access-logfile logs/access.log --error-logfile logs/error.log -p $PORT.proc --worker-class gevent -D
REGISTERED=false; while ! $REGISTERED; do curl -s -X POST "http://127.0.0.1:$PORT/nodes/register" -H "Content-Type: application/json" --data '{"node":"'"$(cat config.json | jq .registration_node -r)"'"}' && REGISTERED=true; done

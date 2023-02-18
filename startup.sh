#!/bin/bash
[ $1 ] && PORT="$1" || PORT="8000"
gunicorn app:app -b 0.0.0.0:$PORT --access-logfile logs/access.log --error-logfile logs/error.log -p proc --worker-class gevent -D
while ! [ $REGISTERED ]; do curl -s -X POST "http://127.0.0.1:$PORT/nodes/register" -H "Content-Type: application/json" --data '{"node":"'"$(cat config.json | jq .registration_node -r)"'"}' && REGISTERED=true; done
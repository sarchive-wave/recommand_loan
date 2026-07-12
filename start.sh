#!/bin/bash
cd "$(dirname "$0")/backend" || exit 1

if [ -f ../server.pid ] && kill -0 "$(cat ../server.pid)" 2>/dev/null; then
  echo "Server already running (PID $(cat ../server.pid))."
  exit 0
fi

nohup python -m uvicorn main:app --host 127.0.0.1 --port 8000 > ../server.log 2>&1 &
echo $! > ../server.pid
sleep 1
echo "Server started (PID $(cat ../server.pid))."
echo "Open http://127.0.0.1:8000"
echo "Logs: server.log"

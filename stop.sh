#!/bin/bash
cd "$(dirname "$0")" || exit 1

if [ -f server.pid ]; then
  PID=$(cat server.pid)
  if kill "$PID" 2>/dev/null; then
    echo "Server stopped (PID $PID)."
  else
    echo "No running process for PID $PID (already stopped?)."
  fi
  rm -f server.pid
else
  echo "server.pid not found. Is the server running? (started via start.sh?)"
fi

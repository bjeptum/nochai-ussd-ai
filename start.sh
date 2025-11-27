#!/bin/bash
echo "Starting NoChai..."
python3 app.py &
sleep 3
ngrok http 5000
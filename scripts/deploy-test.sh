#!/bin/bash
# Deploy to Test Environment
echo "Deploying to TEST environment..."
pkill -f "uvicorn main:app.*8081" || true
sleep 5
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8081 --env-file config/test.env --reload > logs/test.log 2>&1 &
echo "Test environment deployed on port 8081"

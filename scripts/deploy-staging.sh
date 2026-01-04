#!/bin/bash
# Deploy to Staging Environment
echo "Deploying to STAGING environment..."
pkill -f "uvicorn main:app.*8082" || true
sleep 5
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8082 --env-file config/staging.env --workers 2 > logs/staging.log 2>&1 &
echo "Staging environment deployed on port 8082"

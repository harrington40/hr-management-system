#!/bin/bash
# Deploy to Production Environment
echo "⚠️  PRODUCTION DEPLOYMENT"
echo "Creating backup..."
# Add your backup command here
echo "Deploying to PRODUCTION environment..."
pkill -SIGTERM -f "uvicorn main:app.*8080" || true
sleep 10
source venv/bin/activate
nohup uvicorn main:app --host 0.0.0.0 --port 8080 --env-file config/production.env --workers 4 > logs/production.log 2>&1 &
echo "Production environment deployed on port 8080"

#!/bin/bash
# Deploy HRMS app to remote server
# Usage: ./scripts/deploy-remote.sh

set -e  # Exit on any error

# Configuration
REMOTE_USER="dev148"
REMOTE_HOST="109.123.243.148"
REMOTE_DIR="~/hrms"
LOCAL_ENV_FILE=".env"
REPO_URL="https://github.com/harrington40/hr-management-system.git"

echo "🚀 Starting HRMS deployment to $REMOTE_HOST..."

# Check if .env exists locally
if [ ! -f "$LOCAL_ENV_FILE" ]; then
    echo "❌ Error: $LOCAL_ENV_FILE not found in current directory"
    exit 1
fi

echo "📤 Copying .env file to remote server..."
scp "$LOCAL_ENV_FILE" "$REMOTE_USER@$REMOTE_HOST:$REMOTE_DIR/"

echo "🔄 Setting up/updating code on remote server..."
ssh "$REMOTE_USER@$REMOTE_HOST" << EOF
    # Create directory if it doesn't exist
    mkdir -p $REMOTE_DIR
    
    cd $REMOTE_DIR
    
    # Check if it's a git repository
    if [ ! -d ".git" ]; then
        echo "Cloning repository..."
        git clone $REPO_URL .
    else
        echo "Pulling latest changes..."
        git pull origin master
    fi
    
    # Copy .env if it was uploaded
    if [ -f "../.env" ]; then
        cp ../.env .
    fi
    
    # Create virtual environment if it doesn't exist
    if [ ! -d "venv" ]; then
        echo "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    echo "Activating virtual environment..."
    source venv/bin/activate
    
    echo "Installing/updating dependencies..."
    pip install --break-system-packages -r requirements.txt
    
    echo "Restarting application..."
    pkill -f "uvicorn main:app" || true
    sleep 2
    mkdir -p logs
    nohup uvicorn main:app --host 0.0.0.0 --port 8081 > logs/app.log 2>&1 &
    
    echo "✅ Deployment completed!"
    echo "🌐 App should be available at: http://test.transtechologies.com:8081/hrmkit"
    echo "🔧 gRPC service on: localhost:50051"
EOF

echo "🎉 Deployment script completed!"
echo ""
echo "To check app status on server:"
echo "ssh $REMOTE_USER@$REMOTE_HOST 'cd $REMOTE_DIR && ps aux | grep uvicorn'"
echo ""
echo "To view app logs:"
echo "ssh $REMOTE_USER@$REMOTE_HOST 'cd $REMOTE_DIR && tail -f logs/app.log'"
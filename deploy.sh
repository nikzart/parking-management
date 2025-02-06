#!/bin/bash

# Deployment script for Parking Management System
set -e

# Configuration
APP_DIR="/home/zone/parking-system"
VENV_DIR="$APP_DIR/venv"
LOG_DIR="$APP_DIR/logs"
SERVICE_NAME="parking-system"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

echo -e "${GREEN}Starting deployment of Parking Management System...${NC}"

# Create necessary directories
echo -e "${YELLOW}Creating directories...${NC}"
mkdir -p "$APP_DIR"
mkdir -p "$LOG_DIR"

# Install system dependencies
echo -e "${YELLOW}Installing system dependencies...${NC}"
sudo apt update
sudo apt install -y python3-pip python3-venv nginx

# Set up Python virtual environment
echo -e "${YELLOW}Setting up Python virtual environment...${NC}"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Copy application files
echo -e "${YELLOW}Copying application files...${NC}"
rsync -av --exclude 'venv' --exclude '__pycache__' --exclude '*.pyc' ./ "$APP_DIR/"

# Install build dependencies and application
echo -e "${YELLOW}Installing Python dependencies...${NC}"
cd "$APP_DIR"
pip install --upgrade pip
pip install hatchling
pip install -e .

# Create production environment file
echo -e "${YELLOW}Creating production environment file...${NC}"
cat > "$APP_DIR/.env" << EOL
# API Settings
SECRET_KEY=$(openssl rand -hex 32)
API_V1_STR=/api/v1
PROJECT_NAME=Parking Management System
VERSION=1.0.0

# Security
ACCESS_TOKEN_EXPIRE_MINUTES=60
API_KEY_NAME=X-API-Key

# Database
SQLITE_DATABASE_URL=sqlite:///$APP_DIR/parking_system.db

# Rate Limiting
RATE_LIMIT_PER_MINUTE=100
MAX_WEBSOCKET_CONNECTIONS=5

# Data Retention
DEFAULT_RETENTION_HOURS=24

# CORS Settings
BACKEND_CORS_ORIGINS=["http://localhost:3000"]

# Logging
LOG_LEVEL=INFO
LOG_FORMAT=%(asctime)s - %(name)s - %(levelname)s - %(message)s

# Monitoring
ENABLE_METRICS=true
METRICS_PORT=9090

# Development Settings
DEBUG=false
RELOAD=false
EOL

# Create systemd service file
echo -e "${YELLOW}Creating systemd service...${NC}"
sudo tee /etc/systemd/system/$SERVICE_NAME.service << EOL
[Unit]
Description=Parking Management System
After=network.target

[Service]
User=zone
Group=zone
WorkingDirectory=$APP_DIR
Environment="PATH=$VENV_DIR/bin"
Environment="PYTHONPATH=$APP_DIR"
ExecStart=$VENV_DIR/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
EOL

# Setup Nginx configuration
echo -e "${YELLOW}Configuring Nginx...${NC}"
sudo tee /etc/nginx/sites-available/$SERVICE_NAME << EOL
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
    }

    location /metrics {
        proxy_pass http://localhost:9090;
    }
}
EOL

# Enable Nginx site
sudo ln -sf /etc/nginx/sites-available/$SERVICE_NAME /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
export PYTHONPATH=$APP_DIR
$VENV_DIR/bin/alembic upgrade head

# Reload systemd and start services
echo -e "${YELLOW}Starting services...${NC}"
sudo systemctl daemon-reload
sudo systemctl enable $SERVICE_NAME
sudo systemctl restart $SERVICE_NAME
sudo systemctl restart nginx

echo -e "${GREEN}Deployment completed successfully!${NC}"
echo -e "${GREEN}The application is now running at http://$(curl -s ifconfig.me)${NC}"
echo -e "${GREEN}Metrics are available at http://$(curl -s ifconfig.me)/metrics${NC}"

# Display service status
echo -e "${YELLOW}Service status:${NC}"
sudo systemctl status $SERVICE_NAME --no-pager
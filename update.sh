#!/bin/bash

# Update script for Parking Management System
set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

REPO_URL="https://github.com/nikzart/parking-management.git"
APP_DIR="/home/zone/parking-system"
VENV_DIR="$APP_DIR/venv"
BACKUP_DIR="/home/zone/parking-system-backup-$(date +%Y%m%d_%H%M%S)"

# Change to home directory for safety
cd /home/zone

echo -e "${GREEN}Starting update of Parking Management System...${NC}"

# Check if git is installed
if ! command -v git &> /dev/null; then
    echo -e "${YELLOW}Installing git...${NC}"
    sudo apt update
    sudo apt install -y git
fi

# Backup existing env file and database if they exist
echo -e "${YELLOW}Creating backup...${NC}"
if [ -d "$APP_DIR" ]; then
    mkdir -p "$BACKUP_DIR"
    if [ -f "$APP_DIR/.env" ]; then
        cp "$APP_DIR/.env" "$BACKUP_DIR/"
    fi
    if [ -f "$APP_DIR/parking_system.db" ]; then
        cp "$APP_DIR/parking_system.db" "$BACKUP_DIR/"
    fi
    if [ -d "$APP_DIR/data" ]; then
        cp -r "$APP_DIR/data" "$BACKUP_DIR/"
    fi
    echo -e "${GREEN}Backup created at $BACKUP_DIR${NC}"
fi

# Remove existing directory and clone fresh
echo -e "${YELLOW}Cloning latest code...${NC}"
rm -rf "$APP_DIR"
git clone $REPO_URL "$APP_DIR"

# Move to app directory
cd "$APP_DIR" || exit 1

# Create and activate virtual environment
echo -e "${YELLOW}Setting up Python environment...${NC}"
python3 -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"

# Install dependencies
echo -e "${YELLOW}Installing dependencies...${NC}"
pip install --upgrade pip
pip install -r requirements.txt

# Restore .env file if it existed in backup
if [ -f "$BACKUP_DIR/.env" ]; then
    echo -e "${YELLOW}Restoring .env file...${NC}"
    cp "$BACKUP_DIR/.env" "$APP_DIR/"
else
    echo -e "${YELLOW}Creating new .env file...${NC}"
    cp .env.example .env
    # Generate new secret key
    SECRET_KEY=$(openssl rand -hex 32)
    sed -i "s/your-secret-key-here/$SECRET_KEY/" .env
fi

# Restore database if it existed in backup
if [ -f "$BACKUP_DIR/parking_system.db" ]; then
    echo -e "${YELLOW}Restoring database...${NC}"
    cp "$BACKUP_DIR/parking_system.db" "$APP_DIR/"
fi

# Restore data directory if it existed in backup
if [ -d "$BACKUP_DIR/data" ]; then
    echo -e "${YELLOW}Restoring data directory...${NC}"
    cp -r "$BACKUP_DIR/data" "$APP_DIR/"
fi

# Create logs directory if it doesn't exist
mkdir -p "$APP_DIR/logs"

# Run database migrations
echo -e "${YELLOW}Running database migrations...${NC}"
export PYTHONPATH=$APP_DIR
alembic upgrade head

# Restart the service
echo -e "${YELLOW}Restarting service...${NC}"
sudo systemctl restart parking-system

echo -e "${GREEN}Update completed successfully!${NC}"
echo -e "${GREEN}Backup stored at: $BACKUP_DIR${NC}"
echo -e "${YELLOW}Service status:${NC}"
sudo systemctl status parking-system --no-pager

# Return to home directory
cd /home/zone
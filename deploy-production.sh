#!/bin/bash

# WealthFlow Production Deployment Script
# Use this script to deploy/update WealthFlow on the VPS
# Assumes Docker, Docker Compose, Git, and Nginx are already installed

set -e

echo "================================="
echo "WealthFlow Production Deployment"
echo "================================="

# Check if we're in the right directory
if [ ! -f "docker-compose.prod.yml" ]; then
    echo "Error: docker-compose.prod.yml not found!"
    echo "Please run this script from the WealthFlow root directory"
    exit 1
fi

# Pull latest changes
echo "Pulling latest changes from GitHub..."
git pull origin master

# Create backend .env file if it doesn't exist
if [ ! -f "backend/.env" ]; then
    echo "Creating backend .env file..."

    # Generate a secure SECRET_KEY
    SECRET_KEY=$(openssl rand -hex 32)

    cat > backend/.env <<EOF
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow

# Security
SECRET_KEY=${SECRET_KEY}
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS - Update with your domain
BACKEND_CORS_ORIGINS=["http://72.61.233.12","https://72.61.233.12","http://wealthflow.fun","https://wealthflow.fun","http://localhost:5173"]

# Email (Optional)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=True
EMAILS_FROM_EMAIL=noreply@wealthflow.com
EMAILS_FROM_NAME=WealthFlow

# AI Integration (Optional)
OPENAI_API_KEY=
EOF
    echo "✓ Backend .env file created with secure SECRET_KEY"
else
    echo "✓ Backend .env file already exists"
fi

# Create frontend .env file if it doesn't exist
if [ ! -f "frontend/.env" ]; then
    echo "Creating frontend .env file..."
    cat > frontend/.env <<EOF
PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
EOF
    echo "✓ Frontend .env file created"
else
    echo "✓ Frontend .env file already exists"
fi

# Stop existing containers
echo "Stopping existing containers..."
docker-compose -f docker-compose.prod.yml down

# Build and start containers
echo "Building and starting Docker containers..."
docker-compose -f docker-compose.prod.yml build --no-cache
docker-compose -f docker-compose.prod.yml up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Check container status
echo ""
echo "Container Status:"
echo "================================="
docker-compose -f docker-compose.prod.yml ps

# Check logs for errors
echo ""
echo "Recent Backend Logs:"
echo "================================="
docker-compose -f docker-compose.prod.yml logs --tail=20 backend

echo ""
echo "Recent Frontend Logs:"
echo "================================="
docker-compose -f docker-compose.prod.yml logs --tail=20 frontend

echo ""
echo "================================="
echo "Deployment Complete!"
echo "================================="
echo ""
echo "Your application should be running at:"
echo "  Frontend: http://72.61.233.12 (or http://wealthflow.fun)"
echo "  Backend API: http://72.61.233.12:8003"
echo "  API Docs: http://72.61.233.12:8003/docs"
echo ""
echo "To view logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f"
echo ""
echo "To view specific service logs:"
echo "  docker-compose -f docker-compose.prod.yml logs -f backend"
echo "  docker-compose -f docker-compose.prod.yml logs -f frontend"
echo ""
echo "To restart services:"
echo "  docker-compose -f docker-compose.prod.yml restart"
echo ""
echo "To stop everything:"
echo "  docker-compose -f docker-compose.prod.yml down"
echo ""

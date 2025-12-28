#!/bin/bash

# WealthFlow VPS Deployment Script
# This script will deploy the WealthFlow application to your VPS

set -e

echo "================================="
echo "WealthFlow VPS Deployment"
echo "================================="

# Update system packages
echo "Updating system packages..."
apt-get update
apt-get upgrade -y

# Install Docker
echo "Installing Docker..."
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    rm get-docker.sh
    systemctl start docker
    systemctl enable docker
else
    echo "Docker already installed"
fi

# Install Docker Compose
echo "Installing Docker Compose..."
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
else
    echo "Docker Compose already installed"
fi

# Install Git
echo "Installing Git..."
if ! command -v git &> /dev/null; then
    apt-get install -y git
else
    echo "Git already installed"
fi

# Install Nginx
echo "Installing Nginx..."
if ! command -v nginx &> /dev/null; then
    apt-get install -y nginx
    systemctl start nginx
    systemctl enable nginx
else
    echo "Nginx already installed"
fi

# Clone the repository
echo "Cloning WealthFlow repository..."
cd /opt
if [ -d "WealthFlow" ]; then
    echo "Repository already exists, pulling latest changes..."
    cd WealthFlow
    git pull
else
    git clone https://github.com/shyamvijaybalaji/WealthFlow.git
    cd WealthFlow
fi

# Create backend .env file
echo "Creating backend .env file..."
cat > backend/.env <<'EOF'
# Database
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow

# Security - CHANGE THIS IN PRODUCTION
SECRET_KEY=your-production-secret-key-change-this-to-a-long-random-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# CORS
BACKEND_CORS_ORIGINS=["http://72.61.233.12","https://72.61.233.12","http://localhost:5173"]

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

# Create frontend .env file
echo "Creating frontend .env file..."
cat > frontend/.env <<'EOF'
PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
EOF

# Update docker-compose.yml for production
echo "Updating docker-compose.yml..."
cat > docker-compose.yml <<'EOF'
version: '3.8'

services:
  postgres:
    image: postgres:15
    container_name: wealthflow_postgres
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: wealthflow
    ports:
      - "5433:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
    restart: unless-stopped

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: wealthflow_backend
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow
    ports:
      - "8003:8000"
    depends_on:
      - postgres
    restart: unless-stopped
    command: >
      sh -c "
        alembic upgrade head &&
        python scripts/seed_categories.py &&
        uvicorn app.main:app --host 0.0.0.0 --port 8000
      "

  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
    container_name: wealthflow_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
EOF

# Create backend Dockerfile
echo "Creating backend Dockerfile..."
cat > backend/Dockerfile <<'EOF'
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
EOF

# Create frontend Dockerfile
echo "Creating frontend Dockerfile..."
cat > frontend/Dockerfile <<'EOF'
FROM node:20-alpine AS builder

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY . .

# Build the application
RUN npm run build

# Production stage
FROM node:20-alpine

WORKDIR /app

# Copy built application
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules

EXPOSE 3000

CMD ["node", "build"]
EOF

# Generate a secure SECRET_KEY
echo "Generating secure SECRET_KEY..."
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s|your-production-secret-key-change-this-to-a-long-random-string|${SECRET_KEY}|g" backend/.env

# Build and start containers
echo "Building and starting Docker containers..."
docker-compose down
docker-compose build
docker-compose up -d

# Wait for services to be ready
echo "Waiting for services to start..."
sleep 30

# Check container status
echo "Checking container status..."
docker-compose ps

# Configure Nginx reverse proxy
echo "Configuring Nginx..."
cat > /etc/nginx/sites-available/wealthflow <<'EOF'
server {
    listen 80;
    server_name 72.61.233.12;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_cache_bypass $http_upgrade;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8003;
        proxy_http_version 1.1;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF

# Enable Nginx site
ln -sf /etc/nginx/sites-available/wealthflow /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t
systemctl reload nginx

# Configure firewall
echo "Configuring firewall..."
if command -v ufw &> /dev/null; then
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    ufw --force enable
fi

echo "================================="
echo "Deployment Complete!"
echo "================================="
echo ""
echo "Your application is now running at:"
echo "  Frontend: http://72.61.233.12"
echo "  Backend API: http://72.61.233.12:8003"
echo "  API Docs: http://72.61.233.12:8003/docs"
echo ""
echo "Database:"
echo "  PostgreSQL is running on port 5433"
echo ""
echo "Default login credentials:"
echo "  Email: shyam@example.com"
echo "  Password: password123"
echo ""
echo "To view logs:"
echo "  docker-compose logs -f"
echo ""
echo "To stop the application:"
echo "  docker-compose down"
echo ""
echo "To restart the application:"
echo "  docker-compose restart"
echo ""
echo "IMPORTANT SECURITY NOTES:"
echo "1. Change the SECRET_KEY in backend/.env (already generated)"
echo "2. Update CORS origins in backend/.env if using a domain"
echo "3. Set up SSL/HTTPS using Let's Encrypt (certbot)"
echo "4. Change default user password after first login"
echo "5. Consider changing the PostgreSQL password"
echo ""

# WealthFlow VPS Deployment Script for Windows
# Run this script to deploy to your VPS

$VPS_HOST = "72.61.233.12"
$VPS_USER = "root"
$VPS_PASSWORD = "NDSVBdec@2025"

Write-Host "=================================" -ForegroundColor Cyan
Write-Host "WealthFlow VPS Deployment" -ForegroundColor Cyan
Write-Host "=================================" -ForegroundColor Cyan
Write-Host ""

# Upload deployment script to VPS
Write-Host "Uploading deployment script to VPS..." -ForegroundColor Yellow

# Create a temporary expect-like script for SSH
$deployScriptContent = Get-Content "deploy.sh" -Raw

# Use plink (PuTTY) if available, otherwise use native SSH
Write-Host "Connecting to VPS..." -ForegroundColor Yellow
Write-Host "Host: $VPS_HOST" -ForegroundColor Gray
Write-Host ""

# Instructions for manual deployment
Write-Host "AUTOMATED DEPLOYMENT STEPS:" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "Please run the following commands manually:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. Open a new terminal and connect to your VPS:" -ForegroundColor White
Write-Host "   ssh root@72.61.233.12" -ForegroundColor Cyan
Write-Host ""
Write-Host "2. Run the deployment script:" -ForegroundColor White
Write-Host @"
   # Update system
   apt-get update && apt-get upgrade -y

   # Install Docker
   curl -fsSL https://get.docker.com -o get-docker.sh && sh get-docker.sh

   # Install Docker Compose
   curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-`$(uname -s)-`$(uname -m)" -o /usr/local/bin/docker-compose
   chmod +x /usr/local/bin/docker-compose

   # Install Git and Nginx
   apt-get install -y git nginx

   # Clone repository
   cd /opt
   git clone https://github.com/shyamvijaybalaji/WealthFlow.git
   cd WealthFlow

   # Create backend .env
   cat > backend/.env <<'EOF'
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow
SECRET_KEY=`$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://72.61.233.12","https://72.61.233.12"]
OPENAI_API_KEY=
EOF

   # Create frontend .env
   cat > frontend/.env <<'EOF'
PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
EOF

   # Create backend Dockerfile
   cat > backend/Dockerfile <<'EOF'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y gcc postgresql-client && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["sh", "-c", "alembic upgrade head && python scripts/seed_categories.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
EOF

   # Create frontend Dockerfile
   cat > frontend/Dockerfile <<'EOF'
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

FROM node:20-alpine
WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/package*.json ./
COPY --from=builder /app/node_modules ./node_modules
EXPOSE 3000
ENV NODE_ENV=production
CMD ["node", "build"]
EOF

   # Update docker-compose.yml
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
    build: ./backend
    container_name: wealthflow_backend
    ports:
      - "8003:8000"
    depends_on:
      - postgres
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow

  frontend:
    build: ./frontend
    container_name: wealthflow_frontend
    ports:
      - "3000:3000"
    depends_on:
      - backend
    restart: unless-stopped

volumes:
  postgres_data:
EOF

   # Build and start
   docker-compose build
   docker-compose up -d

   # Configure Nginx
   cat > /etc/nginx/sites-available/wealthflow <<'EOF'
server {
    listen 80;
    server_name 72.61.233.12;

    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade `$http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host `$host;
        proxy_cache_bypass `$http_upgrade;
    }

    location /api {
        proxy_pass http://localhost:8003;
        proxy_set_header Host `$host;
        proxy_set_header X-Real-IP `$remote_addr;
    }
}
EOF

   ln -sf /etc/nginx/sites-available/wealthflow /etc/nginx/sites-enabled/
   rm -f /etc/nginx/sites-enabled/default
   nginx -t && systemctl reload nginx

   # Configure firewall
   ufw allow 22/tcp
   ufw allow 80/tcp
   ufw allow 443/tcp
   ufw --force enable

   echo "Deployment complete!"
   docker-compose ps
"@ -ForegroundColor Cyan

Write-Host ""
Write-Host "=================================" -ForegroundColor Green
Write-Host "OR USE AUTOMATED DEPLOYMENT:" -ForegroundColor Green
Write-Host "=================================" -ForegroundColor Green
Write-Host ""
Write-Host "I'll attempt automated deployment now..." -ForegroundColor Yellow

# Attempt to use SSH with password (requires SSH client)
try {
    # Copy deployment script
    Write-Host "Copying deployment script to VPS..." -ForegroundColor Yellow
    $scriptPath = "D:\Financial_Planner\deploy.sh"

    # Use SCP to copy file (you may need to enter password manually)
    & scp $scriptPath "${VPS_USER}@${VPS_HOST}:/tmp/deploy.sh"

    Write-Host "Executing deployment script..." -ForegroundColor Yellow
    & ssh "${VPS_USER}@${VPS_HOST}" "chmod +x /tmp/deploy.sh && /tmp/deploy.sh"

    Write-Host ""
    Write-Host "=================================" -ForegroundColor Green
    Write-Host "Deployment Successful!" -ForegroundColor Green
    Write-Host "=================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Access your application at:" -ForegroundColor Cyan
    Write-Host "  Frontend: http://72.61.233.12" -ForegroundColor White
    Write-Host "  Backend API: http://72.61.233.12:8003" -ForegroundColor White
    Write-Host "  API Docs: http://72.61.233.12:8003/docs" -ForegroundColor White
    Write-Host ""

} catch {
    Write-Host ""
    Write-Host "Automated deployment failed. Please use manual steps above." -ForegroundColor Red
    Write-Host "Error: $_" -ForegroundColor Red
}

Write-Host ""
Write-Host "Press any key to exit..." -ForegroundColor Gray
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")

# WealthFlow VPS Deployment Guide

## Quick Deployment (Copy & Paste)

### Option 1: Automated One-Command Deployment

Connect to your VPS and run this single command:

```bash
ssh root@72.61.233.12
```

Then paste this entire block:

```bash
#!/bin/bash
set -e

echo "=== WealthFlow Deployment Starting ==="

# Update system
apt-get update && apt-get upgrade -y

# Install Docker
if ! command -v docker &> /dev/null; then
    curl -fsSL https://get.docker.com -o get-docker.sh
    sh get-docker.sh
    systemctl start docker && systemctl enable docker
fi

# Install Docker Compose
if ! command -v docker-compose &> /dev/null; then
    curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
    chmod +x /usr/local/bin/docker-compose
fi

# Install dependencies
apt-get install -y git nginx

# Clone repository
cd /opt
if [ -d "WealthFlow" ]; then
    cd WealthFlow && git pull
else
    git clone https://github.com/shyamvijaybalaji/WealthFlow.git
    cd WealthFlow
fi

# Create backend .env
cat > backend/.env <<'ENVEOF'
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://72.61.233.12","https://72.61.233.12","http://localhost:3000"]
SMTP_HOST=
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=
SMTP_TLS=True
EMAILS_FROM_EMAIL=noreply@wealthflow.com
EMAILS_FROM_NAME=WealthFlow
OPENAI_API_KEY=
ENVEOF

# Generate and set SECRET_KEY
SECRET_KEY=$(openssl rand -hex 32)
sed -i "s|SECRET_KEY=.*|SECRET_KEY=$SECRET_KEY|g" backend/.env

# Create frontend .env
cat > frontend/.env <<'ENVEOF'
PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
ENVEOF

# Create backend Dockerfile
cat > backend/Dockerfile <<'DOCKEREOF'
FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["sh", "-c", "alembic upgrade head && python scripts/seed_categories.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
DOCKEREOF

# Create frontend Dockerfile
cat > frontend/Dockerfile <<'DOCKEREOF'
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
ENV ORIGIN=http://72.61.233.12

CMD ["node", "build"]
DOCKEREOF

# Update docker-compose.yml
cat > docker-compose.yml <<'COMPOSEEOF'
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
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres"]
      interval: 10s
      timeout: 5s
      retries: 5

  backend:
    build:
      context: ./backend
      dockerfile: Dockerfile
    container_name: wealthflow_backend
    ports:
      - "8003:8000"
    depends_on:
      postgres:
        condition: service_healthy
    restart: unless-stopped
    environment:
      - DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow
    volumes:
      - ./backend:/app

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
    environment:
      - PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
      - ORIGIN=http://72.61.233.12

volumes:
  postgres_data:
COMPOSEEOF

# Stop existing containers
docker-compose down 2>/dev/null || true

# Build and start containers
echo "Building Docker containers (this may take 5-10 minutes)..."
docker-compose build --no-cache

echo "Starting containers..."
docker-compose up -d

# Wait for services
echo "Waiting for services to start..."
sleep 45

# Check status
docker-compose ps

# Configure Nginx
cat > /etc/nginx/sites-available/wealthflow <<'NGINXEOF'
server {
    listen 80;
    server_name 72.61.233.12;
    client_max_body_size 50M;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
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
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
    }
}
NGINXEOF

# Enable site
ln -sf /etc/nginx/sites-available/wealthflow /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Test and reload Nginx
nginx -t && systemctl reload nginx

# Configure firewall
if command -v ufw &> /dev/null; then
    ufw allow 22/tcp
    ufw allow 80/tcp
    ufw allow 443/tcp
    echo "y" | ufw enable
fi

echo ""
echo "================================="
echo "✅ Deployment Complete!"
echo "================================="
echo ""
echo "🌐 Access your application:"
echo "   Frontend: http://72.61.233.12"
echo "   Backend API: http://72.61.233.12:8003"
echo "   API Docs: http://72.61.233.12:8003/docs"
echo ""
echo "📊 View logs:"
echo "   docker-compose logs -f"
echo ""
echo "🔐 Default credentials:"
echo "   Email: shyam@example.com"
echo "   Password: password123"
echo ""
echo "⚡ Useful commands:"
echo "   docker-compose restart    # Restart all services"
echo "   docker-compose down       # Stop all services"
echo "   docker-compose up -d      # Start all services"
echo "   docker-compose ps         # Check status"
echo ""
```

---

## Option 2: Manual Step-by-Step

### Step 1: Connect to VPS
```bash
ssh root@72.61.233.12
# Password: NDSVBdec@2025
```

### Step 2: Install Docker
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sh get-docker.sh
```

### Step 3: Install Docker Compose
```bash
curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
chmod +x /usr/local/bin/docker-compose
```

### Step 4: Install Git and Nginx
```bash
apt-get update
apt-get install -y git nginx
```

### Step 5: Clone Repository
```bash
cd /opt
git clone https://github.com/shyamvijaybalaji/WealthFlow.git
cd WealthFlow
```

### Step 6: Create Environment Files

Backend `.env`:
```bash
cat > backend/.env <<'EOF'
DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow
SECRET_KEY=$(openssl rand -hex 32)
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
BACKEND_CORS_ORIGINS=["http://72.61.233.12","https://72.61.233.12"]
OPENAI_API_KEY=
EOF
```

Frontend `.env`:
```bash
cat > frontend/.env <<'EOF'
PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
EOF
```

### Step 7: Build and Deploy
```bash
docker-compose build
docker-compose up -d
```

### Step 8: Configure Nginx (see full config in Option 1)

---

## Troubleshooting

### Check Container Status
```bash
docker-compose ps
```

### View Logs
```bash
# All services
docker-compose logs -f

# Specific service
docker-compose logs -f backend
docker-compose logs -f frontend
docker-compose logs -f postgres
```

### Restart Services
```bash
docker-compose restart
```

### Rebuild After Changes
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### Database Issues
```bash
# Access PostgreSQL
docker exec -it wealthflow_postgres psql -U postgres -d wealthflow

# Reset database
docker-compose down -v
docker-compose up -d
```

---

## Security Checklist

- [ ] Change SECRET_KEY in backend/.env (auto-generated during deployment)
- [ ] Update default user password after first login
- [ ] Set up SSL/HTTPS with Let's Encrypt
- [ ] Configure firewall rules (UFW)
- [ ] Change PostgreSQL password
- [ ] Set up automated backups
- [ ] Configure monitoring

---

## SSL Setup (Optional but Recommended)

```bash
# Install Certbot
apt-get install -y certbot python3-certbot-nginx

# Get SSL certificate (replace with your domain)
certbot --nginx -d yourdomain.com

# Auto-renewal is configured automatically
```

---

## Backup Strategy

### Database Backup
```bash
# Create backup
docker exec wealthflow_postgres pg_dump -U postgres wealthflow > backup_$(date +%Y%m%d).sql

# Restore backup
docker exec -i wealthflow_postgres psql -U postgres wealthflow < backup_20240101.sql
```

### Full Backup
```bash
cd /opt/WealthFlow
tar -czf /backup/wealthflow_$(date +%Y%m%d).tar.gz .
```

---

## Monitoring

### Check Resource Usage
```bash
docker stats
```

### Check Disk Space
```bash
df -h
```

### Check Memory
```bash
free -h
```

---

## Updates

### Update Application
```bash
cd /opt/WealthFlow
git pull
docker-compose build
docker-compose up -d
```

### Update System
```bash
apt-get update && apt-get upgrade -y
```

---

## Support

For issues, check:
1. Container logs: `docker-compose logs -f`
2. Nginx logs: `tail -f /var/log/nginx/error.log`
3. System logs: `journalctl -xe`

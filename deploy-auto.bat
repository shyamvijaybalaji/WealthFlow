@echo off
echo ===================================
echo WealthFlow Automated Deployment
echo ===================================
echo.
echo Connecting to VPS: 72.61.233.12
echo.

REM Create a temporary script file
set TEMP_SCRIPT=%TEMP%\wealthflow_deploy.sh

(
echo #!/bin/bash
echo set -e
echo echo "=== WealthFlow Deployment Starting ==="
echo apt-get update ^&^& apt-get upgrade -y
echo if ! command -v docker ^&^> /dev/null; then curl -fsSL https://get.docker.com -o get-docker.sh ^&^& sh get-docker.sh ^&^& systemctl start docker ^&^& systemctl enable docker; fi
echo if ! command -v docker-compose ^&^> /dev/null; then curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s^)-$(uname -m^)" -o /usr/local/bin/docker-compose ^&^& chmod +x /usr/local/bin/docker-compose; fi
echo apt-get install -y git nginx
echo cd /opt
echo if [ -d "WealthFlow" ]; then cd WealthFlow ^&^& git pull; else git clone https://github.com/shyamvijaybalaji/WealthFlow.git ^&^& cd WealthFlow; fi
echo cat ^> backend/.env ^<^<'ENVEOF'
echo DATABASE_URL=postgresql://postgres:postgres@postgres:5432/wealthflow
echo SECRET_KEY=$(openssl rand -hex 32^)
echo ALGORITHM=HS256
echo ACCESS_TOKEN_EXPIRE_MINUTES=30
echo BACKEND_CORS_ORIGINS=[\"http://72.61.233.12\",\"https://72.61.233.12\"]
echo OPENAI_API_KEY=
echo ENVEOF
echo cat ^> frontend/.env ^<^<'ENVEOF'
echo PUBLIC_API_URL=http://72.61.233.12:8003/api/v1
echo ENVEOF
echo docker-compose down 2^>/dev/null ^|^| true
echo docker-compose build --no-cache
echo docker-compose up -d
echo echo "Deployment complete!"
echo docker-compose ps
) > "%TEMP_SCRIPT%"

echo Deployment script created.
echo.
echo ===================================
echo IMPORTANT: Manual Steps Required
echo ===================================
echo.
echo Please follow these steps:
echo.
echo 1. Open a new Command Prompt or PowerShell window
echo.
echo 2. Run: ssh root@72.61.233.12
echo    Password: NDSVBdec@2025
echo.
echo 3. Once connected, paste this command:
echo.
type deploy.sh
echo.
echo ===================================
echo.
echo OR use the detailed guide in DEPLOYMENT.md
echo.
pause

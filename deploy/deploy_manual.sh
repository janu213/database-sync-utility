#!/bin/bash

# Ubuntu 24.04 Manual Deployment Script
# Run with sudo: sudo ./deploy_manual.sh

set -e

echo "--- Starting Deployment on Ubuntu 24.04 ---"

# 1. Update & Install Basic Tools
apt-get update && apt-get upgrade -y
apt-get install -y python3-pip python3-venv nodejs npm nginx curl gnupg build-essential

# 2. Install Microsoft ODBC Driver for MSSQL (Linux)
if ! command -v sqlcmd &> /dev/null; then
    echo "Installing Microsoft ODBC Driver..."
    curl -fsSL https://packages.microsoft.com/keys/microsoft.asc | gpg --dearmor -o /usr/share/keyrings/microsoft-prod.gpg
    curl -fsSL https://packages.microsoft.com/config/ubuntu/24.04/prod.list | tee /etc/apt/sources.list.d/mssql-release.list
    apt-get update
    ACCEPT_EULA=Y apt-get install -y msodbcsql18 mssql-tools18
    echo 'export PATH="$PATH:/opt/mssql-tools18/bin"' >> ~/.bashrc
fi

# 3. Setup Backend
echo "Setting up Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install gunicorn uvicorn
cd ..

# 4. Setup Frontend
echo "Building Frontend..."
cd frontend
npm install
npm run build
cd ..

# 5. Configure Nginx
echo "Configuring Nginx..."
cp deploy/nginx.conf /etc/nginx/sites-available/db-sync
ln -sf /etc/nginx/sites-available/db-sync /etc/nginx/sites-enabled/
rm -f /etc/nginx/sites-enabled/default

# Adjust Nginx root for manual install (root is in frontend/dist)
sed -i 's|/usr/share/nginx/html|'$(pwd)'/frontend/dist|g' /etc/nginx/sites-available/db-sync
systemctl restart nginx

# 6. Create Systemd Service for Backend
echo "Creating Systemd Service..."
cat <<EOF > /etc/systemd/system/db-sync-backend.service
[Unit]
Description=Gunicorn instance to serve Database Sync Backend
After=network.target

[Service]
User=$USER
Group=www-data
WorkingDirectory=$(pwd)/backend
Environment="PATH=$(pwd)/backend/venv/bin"
ExecStart=$(pwd)/backend/venv/bin/gunicorn -w 4 -k uvicorn.workers.UvicornWorker main:app --bind 0.0.0.0:8000

[Install]
WantedBy=multi-user.target
EOF

systemctl daemon-reload
systemctl enable db-sync-backend
systemctl start db-sync-backend

echo "--- Deployment Complete! ---"
echo "Application is available at http://$(hostname -I | awk '{print $1}')"

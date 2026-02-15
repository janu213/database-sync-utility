# Deployment Guide (Ubuntu 24.04)

This guide provides instructions for deploying the Database Sync Utility to an Ubuntu 24.04 server.

## Option 1: Docker (Recommended)

This is the fastest and most reliable method.

### Prerequisites
- Docker and Docker Compose installed on your Ubuntu server.

### Steps
1.  **Transfer Files**: Copy the entire project folder to your server.
2.  **Navigate to Deploy Folder**:
    ```bash
    cd deploy
    ```
3.  **Cleanup & Start**:
    If you have existing containers or errors, run this first:
    ```bash
    docker compose down -v
    ```
    Then start the stack (Note the space: `docker compose` instead of `docker-compose`):
    ```bash
    docker compose up -d --build
    ```
4.  **Access the App**: Open your browser to `http://<your-server-ip>`.

---

## Option 2: Manual Installation

Use this if you prefer to run services directly on the host.

### Steps
1.  **Make the script executable**:
    ```bash
    chmod +x deploy/deploy_manual.sh
    ```
2.  **Run the script with sudo**:
    ```bash
    sudo ./deploy/deploy_manual.sh
    ```
3.  **Access the App**: The script will output your server's IP address.

---

## Troubleshooting

### 1. Docker Build "i/o timeout" or DNS Errors
If you see `lookup registry-1.docker.io: i/o timeout`, your server cannot resolve external addresses.
- **Test Connectivity**: Run `ping -c 3 google.com`.
- **Fix DNS**:
  1. Edit resolv.conf: `sudo nano /etc/resolv.conf`
  2. Add Google DNS: `nameserver 8.8.8.8`
  3. Try the docker-compose command again.

### 2. MSSQL SSL Issues on Linux
Linux uses Microsoft ODBC Driver 18, which defaults to `Encrypt=yes`.
- If connection fails, add `;TrustServerCertificate=yes` to your connection string in the UI.

## Post-Deployment
- **Logs**: Backend logs will be visible via `docker logs backend` or in `/var/log/syslog` for the manual setup.
- **Database**: The SQLite database (`jobs.db`) is stored in `backend/data` (Docker) or `backend/` (Manual).


# Database Sync Utility

A powerful, user-friendly utility to synchronize data from MSSQL (Source) to MySQL (Target) with automated schema mapping and job scheduling.

---

## 🚀 Standard Operating Procedure (SOP)

### 1. Windows Setup (Local Development / Usage)

**Prerequisites:**
- Python 3.10+
- Node.js 18+
- MSSQL and MySQL access

**Steps:**
1.  **Backend Setup**:
    - Open terminal in `backend/`
    - Create virtual environment: `python -m venv venv`
    - Activate venv: `.\venv\Scripts\activate`
    - Install deps: `pip install -r requirements.txt`
    - Start server: `python main.py` (Runs on `http://localhost:8000`)

2.  **Frontend Setup**:
    - Open terminal in `frontend/`
    - Install deps: `npm install`
    - Start dev server: `npm run dev` (Runs on `http://localhost:5173`)

3.  **Usage**:
    - Access the UI, configure your connection, map your columns, and set a sync interval.

---

### 2. Ubuntu 24.04 Setup (Production Deployment)

**Option A: Docker (Recommended)**
*Best for isolation and handling MSSQL drivers effortlessly.*

1.  **Prerequisites**: Docker & Docker Compose installed.
2.  **Steps**:
    ```bash
    cd deploy
    docker compose down -v # Clean start
    docker compose up -d --build
    ```
3.  **Access**: `http://<your-server-ip>`

**Option B: Manual Installation**
*Best if you prefer running on the host OS.*

1.  **Steps**:
    ```bash
    chmod +x deploy/deploy_manual.sh
    sudo ./deploy/deploy_manual.sh
    ```
2.  **Access**: The script will provide the local IP address.

---

## 🛠 Features
- **Smart Mapping**: Automatically match source columns to target columns.
- **Job Dashboard**: Monitor success/failure and last run times.
- **File Logging**: Logs saved to `backend/sync_app.log`.
- **Auto-Table Creation**: Target tables are created automatically if they don't exist.

## 📝 Configuration Tips
- **MSSQL on Linux**: If you see certificate errors, append `;TrustServerCertificate=yes` to your connection string.
- **SQLite**: The job database is stored locally in `backend/jobs.db`.

---
*Created with ❤️ by Sid*

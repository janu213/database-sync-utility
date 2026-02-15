# Test Database Setup

Since I cannot run Docker directly in this environment, here are the instructions to set up the test databases manually or via Docker Desktop if you have it installed.

## 1. Docker Compose (Recommended)

Save the following as `docker-compose.yml` in the project root:

```yaml
version: '3.8'
services:
  mssql_source:
    image: mcr.microsoft.com/mssql/server:2022-latest
    container_name: mssql_source
    environment:
      - ACCEPT_EULA=Y
      - SA_PASSWORD=YourStrong!Passw0rd
    ports:
      - "1433:1433"
  
  mysql_target:
    image: mysql:8.0
    container_name: mysql_target
    environment:
      - MYSQL_ROOT_PASSWORD=rootpassword
      - MYSQL_DATABASE=target_db
    ports:
      - "3306:3306"
```

Run:
```bash
docker-compose up -d
```

## 2. Seed Data

Run the provided python script to create the `Users` table in MSSQL:
```bash
python seed_data.py
```

## 3. Connection Details for App

### Source (MSSQL)
- **Host**: `localhost`
- **Port**: `1433`
- **User**: `sa`
- **Password**: `YourStrong!Passw0rd`
- **Database**: `source_db`

### Target (MySQL)
- **Host**: `localhost`
- **Port**: `3306`
- **User**: `root`
- **Password**: `rootpassword`
- **Database**: `target_db`

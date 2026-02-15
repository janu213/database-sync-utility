import requests
import pymysql
import time
import json

BASE_URL = "http://127.0.0.1:8000/api"

SOURCE_CONFIG = {
    "type": "mssql",
    "host": "localhost",
    "port": 1433,
    "user": "sa",
    "password": "YourStrong!Passw0rd",
    "database": "source_db"
}

TARGET_CONFIG = {
    "type": "mysql",
    "host": "localhost",
    "port": 3306,
    "user": "root",
    "password": "rootpassword",
    "database": "target_db"
}

def run_e2e():
    print("--- Starting End-to-End Verification ---")

    # 1. Test Source Connection
    print("\n1. Testing Source (MSSQL) Connection via API...")
    try:
        resp = requests.post(f"{BASE_URL}/test-connection", json=SOURCE_CONFIG)
        if resp.status_code == 200:
            print("✅ MSSQL Connection Successful")
        else:
            print(f"❌ MSSQL Connection Failed: {resp.text}")
            return
    except Exception as e:
        print(f"❌ Backend not reachable: {e}")
        return

    # 2. Test Target Connection
    print("\n2. Testing Target (MySQL) Connection via API...")
    resp = requests.post(f"{BASE_URL}/test-connection", json=TARGET_CONFIG)
    if resp.status_code == 200:
        print("✅ MySQL Connection Successful")
    else:
        print(f"❌ MySQL Connection Failed: {resp.text}")
        return

    # 3. Preview Data
    print("\n3. Testing Query Preview...")
    query = "SELECT * FROM Users"
    resp = requests.post(f"{BASE_URL}/preview-query", json={
        "connection": SOURCE_CONFIG,
        "query": query
    })
    if resp.status_code == 200:
        data = resp.json().get("data", [])
        print(f"✅ Preview Successful. Retrieved {len(data)} rows.")
        print(f"   Sample: {data[0] if data else 'None'}")
    else:
        print(f"❌ Preview Failed: {resp.text}")
        return

    # 4. Create Job
    print("\n4. Creating Sync Job...")
    job_payload = {
        "name": "E2E_Test_Job_" + str(int(time.time())),
        "schedule_interval": 1, # 1 minute
        "source_connection": SOURCE_CONFIG,
        "target_connection": TARGET_CONFIG,
        "query": query,
        "target_table": "synced_users_test",
        "mapping": {
            "ID": "ID",
            "Name": "Name",
            "Email": "Email",
            "CreatedAt": "CreatedAt"
        }
    }
    resp = requests.post(f"{BASE_URL}/jobs", json=job_payload)
    if resp.status_code == 200:
        job_id = resp.json().get("id")
        print(f"✅ Job Created Successfully. ID: {job_id}")
    else:
        print(f"❌ Job Creation Failed: {resp.text}")
        return

    # 5. Wait for Sync (Optional - usually scheduler runs immediately or after interval)
    # APScheduler 'interval' trigger runs after the interval.
    # To verify immediately, we might need to manually trigger or wait.
    # Let's wait 65 seconds to be sure.
    print("\n5. Waiting 65 seconds for job to execute...")
    time.sleep(65)

    # 6. Verify MySQL Data Directly
    print("\n6. Verifying Data in MySQL Target...")
    try:
        conn = pymysql.connect(
            host=TARGET_CONFIG["host"],
            user=TARGET_CONFIG["user"],
            password=TARGET_CONFIG["password"],
            database=TARGET_CONFIG["database"],
            port=TARGET_CONFIG["port"],
            cursorclass=pymysql.cursors.DictCursor
        )
        with conn.cursor() as cursor:
            cursor.execute("SELECT COUNT(*) as count FROM synced_users_test")
            result = cursor.fetchone()
            count = result['count']
            print(f"✅ Data Verification Successful!")
            print(f"   Table 'synced_users_test' has {count} rows.")
            
            # Clean up
            cursor.execute("DROP TABLE synced_users_test")
            print("   (Cleaned up test table)")
        conn.close()
    except Exception as e:
        print(f"❌ Data Verification Failed: {e}")

if __name__ == "__main__":
    run_e2e()

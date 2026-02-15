import requests
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

def test_dashboard_flow():
    print("--- Starting Dashboard Flow Verification ---")

    # 1. Create Job
    print("\n1. Creating Sync Job for Dashboard Test...")
    job_payload = {
        "name": "Dashboard_Test_" + str(int(time.time())),
        "schedule_interval": 1, 
        "source_connection": SOURCE_CONFIG,
        "target_connection": TARGET_CONFIG,
        "query": "SELECT TOP 1 * FROM Users", # efficient query
        "target_table": "dashboard_test_table",
        "mapping": {
            "ID": "ID",
            "Name": "Name"
        }
    }
    
    try:
        resp = requests.post(f"{BASE_URL}/jobs", json=job_payload)
        if resp.status_code != 200:
            print(f"❌ Job Creation Failed: {resp.text}")
            return
            
        job_id = resp.json().get("id")
        print(f"✅ Job Created. ID: {job_id}")
    except Exception as e:
        print(f"❌ API unreachable: {e}")
        return

    # 2. Poll for Status Update
    print("\n2. Waiting for Job execution (max 70s)...")
    start_time = time.time()
    
    while time.time() - start_time < 70:
        try:
            resp = requests.get(f"{BASE_URL}/jobs")
            jobs = resp.json()
            
            # Find our job
            my_job = next((j for j in jobs if j["id"] == job_id), None)
            
            if my_job:
                status = my_job.get("last_run_status")
                last_run = my_job.get("last_run_time")
                
                if status == "success":
                    print(f"\n✅ SUCCESS! Job reported status: '{status}'")
                    print(f"   Last Run Time: {last_run}")
                    print(f"   Message: {my_job.get('last_run_message')}")
                    return
                elif status == "failed":
                    print(f"\n❌ FAILED! Job reported status: '{status}'")
                    print(f"   Message: {my_job.get('last_run_message')}")
                    return
                else:
                    print(f"   Waiting... Current status: {status or 'Pending'}", end="\r")
            
            time.sleep(2)
        except Exception as e:
            print(f"Error polling: {e}")
            time.sleep(2)

    print("\n❌ Timeout waiting for job execution.")

if __name__ == "__main__":
    test_dashboard_flow()

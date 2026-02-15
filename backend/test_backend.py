import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_backend():
    print("Testing Backend...")
    
    # 1. Test Connection (expect failure due to dummy creds)
    try:
        resp = requests.post(f"{BASE_URL}/test-connection", json={
            "type": "mssql",
            "host": "localhost",
            "user": "sa",
            "password": "wrongpassword",
            "database": "master"
        })
        print(f"Test Connection: Status {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"Connection test failed to execute: {e}")

    # 2. List Jobs (should be empty)
    try:
        resp = requests.get(f"{BASE_URL}/jobs")
        print(f"List Jobs: Status {resp.status_code}")
        print(f"Response: {resp.text}")
    except Exception as e:
        print(f"List jobs failed: {e}")

if __name__ == "__main__":
    test_backend()

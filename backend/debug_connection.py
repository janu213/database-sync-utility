import pymssql
import pymysql
import sys

def test_mssql(host, port, user, password):
    print(f"\n--- Testing MSSQL ({host}:{port}) ---")
    try:
        conn = pymssql.connect(
            server=host,
            user=user,
            password=password,
            port=port,
            login_timeout=10
        )
        print("SUCCESS: Connected to MSSQL!")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILURE: {e}")
        return False

def test_mysql(host, port, user, password):
    print(f"\n--- Testing MySQL ({host}:{port}) ---")
    try:
        conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            port=port,
            connect_timeout=10
        )
        print("SUCCESS: Connected to MySQL!")
        conn.close()
        return True
    except Exception as e:
        print(f"FAILURE: {e}")
        return False

if __name__ == "__main__":
    print("This script helps debug connection issues.")
    
    # MSSQL defaults from docker-compose
    mssql_host = input("Enter MSSQL Host [localhost]: ") or "localhost"
    mssql_port = int(input("Enter MSSQL Port [1433]: ") or 1433)
    mssql_user = input("Enter MSSQL User [sa]: ") or "sa"
    mssql_password = input("Enter MSSQL Password [YourStrong!Passw0rd]: ") or "YourStrong!Passw0rd"

    # MySQL defaults form docker-compose
    # mysql_host = "localhost" ... skip for now if only source is failing
    
    print("\nAttempting MSSQL connection...")
    test_mssql(mssql_host, mssql_port, mssql_user, mssql_password)
    
    if mssql_host == "localhost":
        print("\nTrying 127.0.0.1 as alternative...")
        test_mssql("127.0.0.1", mssql_port, mssql_user, mssql_password)

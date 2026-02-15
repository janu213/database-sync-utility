import pymssql
import time

def seed_mssql():
    conn = None
    retries = 0
    while retries < 10:
        try:
            print(f"Connecting to MSSQL (Attempt {retries+1})...")
            conn = pymssql.connect(
                server='localhost',
                user='sa',
                password='YourStrong!Passw0rd',
                database='master',
                port=1433,
                autocommit=True
            )
            print("Connected!")
            break
        except Exception as e:
            print(f"Waiting for MSSQL... {e}")
            time.sleep(5)
            retries += 1

    if not conn:
        print("Could not connect to MSSQL.")
        return

    try:
        cursor = conn.cursor()
        
        # Create Database
        try:
            cursor.execute("CREATE DATABASE source_db")
            print("Created source_db")
        except:
            print("source_db already exists")

        # Switch to source_db
        conn.close()
        conn = pymssql.connect(
            server='localhost',
            user='sa',
            password='YourStrong!Passw0rd',
            database='source_db',
            port=1433,
            autocommit=True
        )
        cursor = conn.cursor()

        # Create Table
        cursor.execute("""
            IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='Users' AND xtype='U')
            CREATE TABLE Users (
                ID INT PRIMARY KEY,
                Name VARCHAR(100),
                Email VARCHAR(100),
                CreatedAt DATETIME DEFAULT GETDATE()
            )
        """)
        print("Created Users table")

        # Insert Data
        cursor.execute("TRUNCATE TABLE Users")
        cursor.execute("""
            INSERT INTO Users (ID, Name, Email) VALUES 
            (1, 'Alice Smith', 'alice@example.com'),
            (2, 'Bob Jones', 'bob@example.com'),
            (3, 'Charlie Brown', 'charlie@example.com'),
            (4, 'David Wilson', 'david@example.com'),
            (5, 'Eve Davis', 'eve@example.com')
        """)
        print("Inserted sample data")
        
    finally:
        if conn: conn.close()

if __name__ == "__main__":
    seed_mssql()

from services.connector import DatabaseConnector
from models import JobCreate, DBConnection
from typing import List, Dict, Any
import pandas as pd

class DataExecutor:
    @staticmethod
    def run_job(job: JobCreate):
        # 1. Fetch data from source
        print(f"Fetching data from source for job: {job.name}")
        source_data = DatabaseConnector.execute_query(job.source_connection, job.query)
        
        if not source_data:
            print("No data found in source.")
            return
            
        # 2. Map data
        # We assume source_data is list of dicts.
        # Mapping: { "source_col": "target_col" }
        mapped_data = []
        for row in source_data:
            new_row = {}
            for source_col, target_col in job.mapping.items():
                if source_col in row:
                    new_row[target_col] = row[source_col]
            mapped_data.append(new_row)
            
        if not mapped_data:
            print("No data to map.")
            return

        # 3. Insert into target
        print(f"Inserting {len(mapped_data)} rows into target table: {job.target_table}")
        
        # Ensure table exists
        # We use the columns from the first row of mapped data
        columns = list(mapped_data[0].keys())
        DatabaseConnector.create_table_if_not_exists(job.target_connection, job.target_table, columns)
        
        DatabaseConnector.insert_data(job.target_connection, job.target_table, mapped_data)
        print("Job completed successfully.")

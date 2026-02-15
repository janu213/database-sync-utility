import pymssql
import pymysql
import pandas as pd
from typing import List, Dict, Any, Tuple
from models import DBConnection

class DatabaseConnector:
    @staticmethod
    def get_connection(config: DBConnection):
        if config.type == 'mssql':
            return pymssql.connect(
                server=config.host,
                user=config.user,
                password=config.password,
                database=config.database,
                port=config.port or 1433,
                as_dict=True
            )
        elif config.type == 'mysql':
            return pymysql.connect(
                host=config.host,
                user=config.user,
                password=config.password,
                database=config.database,
                port=config.port or 3306,
                cursorclass=pymysql.cursors.DictCursor
            )
        else:
            raise ValueError(f"Unsupported database type: {config.type}")

    @staticmethod
    def test_connection(config: DBConnection) -> bool:
        try:
            conn = DatabaseConnector.get_connection(config)
            conn.close()
            return True
        except Exception as e:
            print(f"Connection failed: {e}")
            raise e

    @staticmethod
    def execute_query(config: DBConnection, query: str) -> List[Dict[str, Any]]:
        conn = DatabaseConnector.get_connection(config)
        try:
            with conn.cursor() as cursor:
                cursor.execute(query)
                return cursor.fetchall()
        finally:
            conn.close()

    @staticmethod
    def get_preview(config: DBConnection, query: str, limit: int = 10) -> List[Dict[str, Any]]:
        # Modify query to limit results if possible, or just fetch many and slice
        # Ideally, we should wrap the query. For now, simple fetch.
        # MSSQL: SELECT TOP N ...
        # MySQL: ... LIMIT N
        # But parsing query is hard. We'll just fetchall().
        # Actually for preview, we might want to use pandas to chunk.
        
        conn = DatabaseConnector.get_connection(config)
        try:
            # simple safe-ish preview
            # Note: This is risky for HUGE queries. 
            # Better to ask user to provide limit or append limit.
            # providing a dumb text-based limit injection:
            
            # Simple cursor execution
            with conn.cursor() as cursor:
                cursor.execute(query)
                # fetch `limit` rows
                rows = cursor.fetchmany(limit)
                return rows
        finally:
            conn.close()
            
    @staticmethod
    def create_table_if_not_exists(config: DBConnection, table: str, columns: List[str]):
        conn = DatabaseConnector.get_connection(config)
        try:
            with conn.cursor() as cursor:
                # Simple table creation with TEXT fields for flexibility
                # In a real app, we'd infer types.
                cols_def = ", ".join([f"{col} TEXT" for col in columns])
                # Add an auto-increment ID if needed? 
                # For now, just the mapped columns.
                # MySQL syntax
                if config.type == 'mysql':
                    sql = f"CREATE TABLE IF NOT EXISTS {table} ({cols_def})"
                else:
                    # MSSQL syntax
                     sql = f"IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='{table}' AND xtype='U') CREATE TABLE {table} ({cols_def})"
                
                cursor.execute(sql)
                conn.commit()
        finally:
            conn.close()

    @staticmethod
    def insert_data(config: DBConnection, table: str, data: List[Dict[str, Any]]):
        if not data:
            return
            
        conn = DatabaseConnector.get_connection(config)
        try:
            with conn.cursor() as cursor:
                # Construct INSERT statement
                columns = list(data[0].keys())
                placeholders = ", ".join(["%s"] * len(columns))
                col_names = ", ".join(columns)
                
                sql = f"INSERT INTO {table} ({col_names}) VALUES ({placeholders})"
                
                values = []
                for row in data:
                    values.append([row.get(c) for c in columns])
                    
                cursor.executemany(sql, values)
                conn.commit()
        finally:
            conn.close()

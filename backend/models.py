from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class DBConnection(BaseModel):
    type: str # 'mssql' or 'mysql'
    host: str
    port: Optional[int] = None
    user: str
    password: str
    database: str

class QueryRequest(BaseModel):
    connection: DBConnection
    query: str

class MappingRequest(BaseModel):
    source_connection: DBConnection
    target_connection: DBConnection
    query: str
    target_table: str
    mapping: Dict[str, str] # source_col -> target_col

class JobCreate(BaseModel):
    name: str
    schedule_interval: int # minutes
    source_connection: DBConnection
    target_connection: DBConnection
    query: str
    target_table: str
    mapping: Dict[str, str]

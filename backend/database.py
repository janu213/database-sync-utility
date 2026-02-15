from sqlalchemy import create_engine, Column, Integer, String, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL = "sqlite:///./jobs.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

class JobModel(Base):
    __tablename__ = "jobs"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    schedule_interval = Column(Integer) # minutes
    source_connection = Column(JSON)
    target_connection = Column(JSON)
    query = Column(String)
    target_table = Column(String)
    mapping = Column(JSON)
    status = Column(String, default="active") # active, paused
    last_run_time = Column(String, nullable=True)
    last_run_status = Column(String, nullable=True) # "success", "failed"
    last_run_message = Column(String, nullable=True)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Ensure this URL matches your local PostgreSQL credentials[cite: 1]
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost/fastapi"

engine = create_engine(SQLALCHEMY_DATABASE_URL)[cite: 1]

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)[cite: 1]

Base = declarative_base()[cite: 1]

def get_db():
    db = SessionLocal()[cite: 1]
    try:
        yield db[cite: 1]
    finally:
        db.close()[cite: 1]
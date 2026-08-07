from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# The connection string to your local PostgreSQL database
SQLALCHEMY_DATABASE_URL = "postgresql://postgres:password123@localhost/fastapi"

# The engine is responsible for establishing the connection
engine = create_engine(SQLALCHEMY_DATABASE_URL)

# SessionLocal is what we use to talk to the database in our routes
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base is the blueprint that our models will inherit from
Base = declarative_base()
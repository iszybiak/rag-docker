from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import logging

# Logger configuration
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# Downloading database URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")

try:
    # Connecting to the database
    engine = create_engine(DATABASE_URL)

    # Creating session to operation on the database
    Session = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logger.info("Database connection established")
except Exception as e:
    logging.error(f"Database connection error: {e}")

# Base for SQLAlchemy models
Base = declarative_base()

# Document storage table model
class Document(Base):
    __tablename__ = "rag_document"
    id=Column(Integer, primary_key=True, index=True)
    text=Column(String, nullable=False)

# Function to initialize the database (create tables)
def init_db():
    if engine:
        try:
            Base.metadata.create_all(bind=engine)
            logger.info("The tables were created successfully.")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")
    else:
        logger.error("No active database connection. Cannot create tables.")
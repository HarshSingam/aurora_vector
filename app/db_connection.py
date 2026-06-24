from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from loguru import logger 

DATABASE_URL = ("mysql+pymysql://root:Harsh7777@localhost:3306/aurora_vector_db")
#DATABASE_URL = ...

try:
    engine = create_engine(DATABASE_URL , pool_pre_ping=True)

    logger.success("Database engine initialized")

except Exception:
    logger.exception("Failed to initialize database")
    raise

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

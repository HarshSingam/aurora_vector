from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base

DATABASE_URL = (
    "mysql+pymysql://root:Harsh7777@localhost:3306/aurora_vector_db"
)

engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True
)

Base = declarative_base()
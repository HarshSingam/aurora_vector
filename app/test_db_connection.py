from sqlalchemy import text
from db_connection import engine
from loguru import logger

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))

    logger.success("MySQL connection established")

except Exception:
    logger.exception("MySQL connection failed")

    
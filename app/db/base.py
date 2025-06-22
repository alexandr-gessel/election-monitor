# db/base.py

import asyncpg
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if DATABASE_URL is None:
    raise RuntimeError("DATABASE_URL is not set in .env file")

async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield connx
    finally:
        await conn.close()
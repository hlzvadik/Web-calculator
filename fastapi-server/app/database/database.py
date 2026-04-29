import asyncpg


DATABASE_URL = "postgresql://vadik:G31072007m+@localhost/Web-calculator"

async def get_db_connection():
    conn = await asyncpg.connect(DATABASE_URL)
    try:
        yield conn
    finally:
        await conn.close()


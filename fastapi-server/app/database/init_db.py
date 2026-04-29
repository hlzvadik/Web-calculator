import asyncpg
import asyncio

DATABASE_URL = "postgresql://vadik:G31072007m+@localhost/Web-calculator"

async def create_table():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            email TEXT NOT NULL,
            name TEXT,
            hash_password TEXT NOT NULL
        )
    ''')
    await conn.close()

asyncio.run(create_table())

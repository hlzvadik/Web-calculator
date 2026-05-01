import asyncpg
import asyncio

DATABASE_URL = "postgresql://vadik:G31072007m+@localhost/Web-calculator"

async def create_table_users():
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

async def create_table_history():
    conn = await asyncpg.connect(DATABASE_URL)
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS history(
            id SERIAL PRIMARY KEY,
            user_id INTEGER,
            expression TEXT,
            answer TEXT,
            CONSTRAINT fk_history_user FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE ON UPDATE CASCADE
        )
    ''')

    await conn.close()

asyncio.run(create_table_users())
asyncio.run(create_table_history())

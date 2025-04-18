import asyncio
import asyncpg

async def list_tables():
    conn = await asyncpg.connect(user='user', password='password', database='myappdb', host='localhost')
    rows = await conn.fetch("""
        SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';
    """)
    print("Tables in public schema:", [r['table_name'] for r in rows])
    await conn.close()

if __name__ == "__main__":
    asyncio.run(list_tables())

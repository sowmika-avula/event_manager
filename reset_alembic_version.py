import asyncio
import asyncpg

async def set_alembic_version():
    conn = await asyncpg.connect(user='user', password='password', database='myappdb', host='localhost')
    await conn.execute("UPDATE alembic_version SET version_num = 'ef1d775276c0'")
    print("alembic_version reset to ef1d775276c0")
    await conn.close()

if __name__ == "__main__":
    asyncio.run(set_alembic_version())

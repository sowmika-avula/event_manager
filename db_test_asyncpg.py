import asyncio
import asyncpg

async def test_db():
    try:
        conn = await asyncpg.connect(user='user', password='password', database='myappdb', host='localhost')
        print('Connected to PostgreSQL successfully!')
        await conn.close()
    except Exception as e:
        print(f'Failed to connect: {e}')

if __name__ == "__main__":
    asyncio.run(test_db())

from prisma import Prisma
import asyncio

async def create_database():
    prisma = Prisma()
    await prisma.connect()
    print("Database created successfully!")
    await prisma.disconnect()

asyncio.run(create_database())

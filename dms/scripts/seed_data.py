from prisma import Prisma
import asyncio

async def seed_data():
    prisma = Prisma()
    await prisma.connect()

    # Add sample user
    await prisma.user.create({
        "email": "test@example.com",
        "password": "hashed_password"
    })

    print("Data seeded successfully!")
    await prisma.disconnect()

asyncio.run(seed_data())

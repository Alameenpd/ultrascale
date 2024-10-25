from prisma import Prisma
from app.db.client import prisma
from app.schemas.user import UserCreate
from app.utils.hashing import hash_password

async def create_user(user: UserCreate):
    hashed_password = hash_password(user.password)
    return await prisma.user.create({
        "email": user.email,
        "password": hashed_password
    })

async def get_user_by_email(email: str):
    return await prisma.user.find_unique(where={"email": email})

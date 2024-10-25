async def create_message(user_id: int, content: str):
    return await prisma.message.create({
        "userId": user_id,
        "content": content,
        "status": "pending"
    })

async def get_messages_by_user(user_id: int):
    return await prisma.message.find_many(where={"userId": user_id})

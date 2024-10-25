from fastapi import APIRouter, Depends, HTTPException
from app.crud.message import create_message, get_messages_by_user
from app.schemas.message import MessageCreate, MessageOut
from app.services.celery_tasks import send_dm_task
from app.db.client import prisma
from app.services.instagram_dm import InstagramDMAutomation


router = APIRouter()

@router.post("/messages", response_model=MessageOut)
async def send_message(message: MessageCreate, user_id: int):
    new_message = await create_message(user_id=user_id, content=message.content)
    send_dm_task.delay(user_id, message.content)
    return new_message

@router.get("/messages", response_model=list[MessageOut])
async def get_messages(user_id: int):
    messages = await get_messages_by_user(user_id)
    return messages

@router.post("/send-dm")
async def send_instagram_dm(csv_file: str, account_name: str, username_column: str, message_column: str):
    automation = InstagramDMAutomation(
        csv_file=csv_file,
        username_column=username_column,
        message_column=message_column,
        account_name=account_name
    )
    await automation.run_automation()
    return {"detail": "DMs sending initiated"}
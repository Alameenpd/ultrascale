from celery import Celery
from app.services.instagram import send_instagram_dm

celery_app = Celery("tasks", broker="redis://localhost:6379/0")

@celery_app.task
def send_dm_task(user_id: int, content: str):
    send_instagram_dm(user_id=user_id, content=content)

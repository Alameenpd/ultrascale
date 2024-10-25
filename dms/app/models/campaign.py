from pydantic import BaseModel
from datetime import datetime

class Campaign(BaseModel):
    id: int
    user_id: int
    name: str
    csv_file: str
    status: str = "pending"  # e.g., pending, active, completed
    created_at: datetime
    message_template: str

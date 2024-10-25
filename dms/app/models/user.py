from pydantic import BaseModel
from datetime import datetime

class User(BaseModel):
    id: int
    email: str
    password: str
    role: str = "user"
    created_at: datetime

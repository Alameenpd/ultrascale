class Message(BaseModel):
    id: int
    user_id: int
    content: str
    status: str = "pending"
    created_at: datetime

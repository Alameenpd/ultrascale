class Subscription(BaseModel):
    id: int
    user_id: int
    plan: str
    expires_at: datetime

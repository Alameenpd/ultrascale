class SubscriptionCreate(BaseModel):
    plan: str

class SubscriptionOut(BaseModel):
    id: int
    plan: str
    expires_at: datetime

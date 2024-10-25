from pydantic import BaseModel

class CampaignCreate(BaseModel):
    name: str
    csv_file: str
    message_template: str

class CampaignOut(BaseModel):
    id: int
    name: str
    csv_file: str
    message_template: str
    status: str

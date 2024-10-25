from fastapi import APIRouter, HTTPException
from app.crud.campaign import create_campaign, get_campaigns_by_user, run_campaign
from app.schemas.campaign import CampaignCreate, CampaignOut

router = APIRouter()

@router.post("/campaigns", response_model=CampaignOut)
async def create_campaign_route(campaign: CampaignCreate, user_id: int):
    return await create_campaign(user_id=user_id, campaign=campaign)

@router.get("/campaigns", response_model=list[CampaignOut])
async def get_campaigns(user_id: int):
    return await get_campaigns_by_user(user_id)

@router.post("/campaigns/{campaign_id}/run")
async def run_campaign_route(campaign_id: int):
    result = await run_campaign(campaign_id)
    return {"detail": "Campaign started", "result": result}

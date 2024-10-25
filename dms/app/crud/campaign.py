from prisma import Prisma
from app.schemas.campaign import CampaignCreate
from app.services.instagram_dm import InstagramDMAutomation

async def create_campaign(user_id: int, campaign: CampaignCreate):
    return await prisma.campaign.create({
        "userId": user_id,
        "name": campaign.name,
        "csvFile": campaign.csv_file,
        "messageTemplate": campaign.message_template,
        "status": "pending",
    })

async def get_campaigns_by_user(user_id: int):
    return await prisma.campaign.find_many(where={"userId": user_id})

async def run_campaign(campaign_id: int):
    campaign = await prisma.campaign.find_unique(where={"id": campaign_id})
    if not campaign:
        raise HTTPException(status_code=404, detail="Campaign not found")

    automation = InstagramDMAutomation(
        csv_file=campaign.csvFile,
        username_column="username",
        message_column="message",
        account_name="account_name"  # Replace with dynamic logic for account
    )
    await automation.run_automation(campaign.messageTemplate)
    await prisma.campaign.update(
        where={"id": campaign_id},
        data={"status": "completed"}
    )
    return {"detail": "Campaign executed"}

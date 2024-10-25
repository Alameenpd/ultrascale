from fastapi import APIRouter, HTTPException
from app.crud.subscription import create_subscription, get_subscription_by_user
from app.schemas.subscription import SubscriptionCreate, SubscriptionOut
from datetime import datetime, timedelta
from fastapi import APIRouter, Request, HTTPException
from app.config import settings
import stripe

stripe.api_key = settings.stripe_secret_key

router = APIRouter()

@router.post("/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.stripe_webhook_secret
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail="Invalid payload")
    except stripe.error.SignatureVerificationError as e:
        raise HTTPException(status_code=400, detail="Invalid signature")

    # Handle the event
    if event['type'] == 'invoice.payment_succeeded':
        handle_payment_success(event)
    elif event['type'] == 'customer.subscription.deleted':
        handle_subscription_cancel(event)

    return {"status": "success"}


router = APIRouter()

@router.post("/subscriptions", response_model=SubscriptionOut)
async def create_user_subscription(subscription: SubscriptionCreate, user_id: int):
    expires_at = datetime.utcnow() + timedelta(days=30)  # Assuming a monthly subscription
    return await create_subscription(user_id=user_id, plan=subscription.plan, expires_at=expires_at)

@router.get("/subscriptions", response_model=SubscriptionOut)
async def get_user_subscription(user_id: int):
    subscription = await get_subscription_by_user(user_id)
    if not subscription:
        raise HTTPException(status_code=404, detail="Subscription not found")
    return subscription

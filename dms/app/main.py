from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from redis import Redis
from app.db.client import prisma
from app.config import settings
from app.routers import auth, users, messages, subscriptions, campaigns
from app.utils.error_handlers import register_exception_handlers
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("ultrascale-backend")

# Initialize FastAPI app
app = FastAPI(
    title="Ultrascale DM Sender",
    description="A campaign-based Instagram DM automation tool",
    version="1.0.0"
)

# Middleware for CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update with allowed origins for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Register custom exception handlers
register_exception_handlers(app)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(users.router, prefix="/users", tags=["Users"])
app.include_router(messages.router, prefix="/messages", tags=["Messages"])
app.include_router(subscriptions.router, prefix="/subscriptions", tags=["Subscriptions"])
app.include_router(campaigns.router, prefix="/campaigns", tags=["Campaigns"])

# Connect to the database and Redis on startup
@app.on_event("startup")
async def startup_event():
    await prisma.connect()
    logger.info("Connected to the database")
    await FastAPILimiter.init(Redis.from_url("redis://localhost:6379"))

# Graceful shutdown
@app.on_event("shutdown")
async def shutdown_event():
    await prisma.disconnect()
    logger.info("Disconnected from the database")

# Example health check endpoint
@app.get("/health", tags=["Health"], dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def health_check():
    return {"status": "Healthy"}

# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

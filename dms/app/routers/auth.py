from fastapi import APIRouter, HTTPException, Depends
from app.schemas.user import UserCreate, UserLogin
from app.crud.user import create_user, get_user_by_email
from app.utils.jwt import create_access_token

router = APIRouter()

@router.post("/signup", response_model=UserOut)
async def signup(user: UserCreate):
    existing_user = await get_user_by_email(user.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    created_user = await create_user(user)
    return created_user

@router.post("/login")
async def login(user: UserLogin):
    existing_user = await get_user_by_email(user.email)
    if not existing_user or not existing_user.verify_password(user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token({"sub": existing_user.id})
    return {"access_token": access_token, "token_type": "bearer"}

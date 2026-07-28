from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from src.auth.security import create_access_token

from src.auth.models import (
    create_user,
    get_user_by_email,
    verify_password
)

router = APIRouter(prefix="/auth", tags=["Authentication"])


class UserSignup(BaseModel):
    name: str
    email: str
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(user: UserSignup):

    existing = get_user_by_email(user.email)

    if existing:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    create_user(
        user.name,
        user.email,
        user.password
    )

    return {
        "message": "User registered successfully"
    }


@router.post("/login")
def login(user: UserLogin):

    db_user = get_user_by_email(user.email)

    if not db_user:
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    if not verify_password(
        user.password,
        db_user["password"]
    ):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password"
        )

    token = create_access_token(
        {
            "sub": db_user["email"]
        }
    )

    return {
        "message": "Login successful",
        "access_token": token,
        "token_type": "bearer",
        "user": {
            "id": db_user["id"],
            "name": db_user["name"],
            "email": db_user["email"],
            "role": db_user["role"]
        }
    }
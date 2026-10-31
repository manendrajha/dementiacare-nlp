
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from app.database.connection import database
from app.schemas.user import (
    UserRegister,
    UserLogin,
    UserResponse,
    TokenResponse
)
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token
)
from app.core.dependencies import get_current_user


router = APIRouter(
    prefix="/api/auth",
    tags=["Authentication"]
)

user_collection = database["users"]


def format_user(user):
    return UserResponse(
        id=str(user["_id"]),
        name=user["name"],
        email=user["email"],
        role=user["role"],
        created_at=user["created_at"].isoformat()
    )


@router.post(
    "/register",
    response_model=TokenResponse,
    status_code=status.HTTP_201_CREATED
)
async def register(user: UserRegister):

    email = str(user.email).lower().strip()

    # Ensure email addresses are unique.
    await user_collection.create_index(
        "email",
        unique=True
    )

    existing_user = await user_collection.find_one({
        "email": email
    })

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    document = {
        "name": user.name.strip(),
        "email": email,
        "password": hash_password(user.password),
        "role": user.role,
        "created_at": datetime.now(timezone.utc)
    }

    try:
        result = await user_collection.insert_one(document)
    except DuplicateKeyError:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="An account with this email already exists"
        )

    saved_user = await user_collection.find_one({
        "_id": result.inserted_id
    })

    token = create_access_token(
        str(saved_user["_id"]),
        saved_user["role"]
    )

    return TokenResponse(
        access_token=token,
        user=format_user(saved_user)
    )


@router.post(
    "/login",
    response_model=TokenResponse
)
async def login(credentials: UserLogin):

    email = str(credentials.email).lower().strip()

    user = await user_collection.find_one({
        "email": email
    })

    if (
        not user
        or not verify_password(
            credentials.password,
            user["password"]
        )
    ):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    token = create_access_token(
        str(user["_id"]),
        user["role"]
    )

    return TokenResponse(
        access_token=token,
        user=format_user(user)
    )


@router.get("/me", response_model=UserResponse)
async def get_profile(
    current_user=Depends(get_current_user)
):
    return format_user(current_user)


from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
import jwt

from app.database.connection import database
from app.core.security import decode_access_token


security = HTTPBearer(auto_error=False)


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    unauthorized = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or missing authentication token",
        headers={"WWW-Authenticate": "Bearer"}
    )

    if credentials is None:
        raise unauthorized

    try:
        payload = decode_access_token(credentials.credentials)
        user_id = payload.get("sub")

        if not user_id or not ObjectId.is_valid(user_id):
            raise unauthorized

    except (jwt.InvalidTokenError, ValueError):
        raise unauthorized

    user = await database["users"].find_one({
        "_id": ObjectId(user_id)
    })

    if not user:
        raise unauthorized

    # Never expose the stored password hash to route handlers.
    user.pop("password", None)

    return user


def require_role(*allowed_roles):
    async def role_checker(
        current_user=Depends(get_current_user)
    ):
        if current_user.get("role") not in allowed_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have permission to access this resource"
            )

        return current_user

    return role_checker

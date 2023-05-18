from typing import Optional

from fastapi import Request, HTTPException, Header, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from apps.auth.auth_handler import decode_jwt
from apps.user.models import UserSchema
from db import db

users_collection = db['users']


class JWTBearer(HTTPBearer):
    def __init__(self, auto_error: bool = True):
        super(JWTBearer, self).__init__(auto_error=auto_error)

    async def __call__(self, request: Request):
        credentials: HTTPAuthorizationCredentials = await super(JWTBearer, self).__call__(request)
        if credentials:
            if not credentials.scheme == "Bearer":
                raise HTTPException(status_code=403, detail="Invalid authentication scheme.")
            if not self.verify_jwt(credentials.credentials):
                raise HTTPException(status_code=403, detail="Invalid token or expired token.")
            return credentials.credentials
        else:
            raise HTTPException(status_code=403, detail="Invalid authorization code.")

    def verify_jwt(self, jwtoken: str) -> bool:
        is_token_valid: bool = False

        try:
            payload = decode_jwt(jwtoken)
        except:
            payload = None
        if payload:
            is_token_valid = True
        return is_token_valid


async def get_jwt_subject(authorization: Optional[str] = Header(None)):
    if not authorization:
        raise HTTPException(status_code=401, detail="Authorization header is missing")
    try:
        token = authorization.split()[1]
        payload = decode_jwt(token)
        return users_collection.find_one({"email": payload.get("user_email")})
    except:
        raise HTTPException(status_code=401, detail="Invalid token")


async def get_current_admin_user(current_user: dict = Depends(get_jwt_subject)):
    if not current_user["is_admin"]:
        raise HTTPException(status_code=403, detail="You are not authorized to perform this action")
    return current_user

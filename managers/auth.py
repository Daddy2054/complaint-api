from typing import Optional
#import dotenv
from fastapi import HTTPException #, Request
from starlette.requests import Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

import jwt

from datetime import datetime, timedelta, timezone
import os
from db import database
from models import user
from models.enums import RoleType

#dotenv.load_dotenv()
secret_key = os.getenv('SECRET_KEY')

class AuthManager:
    @staticmethod
    def encode_token(user):
        try:

            # payload = {
            #     'sub': user["id"],
            #     'exp': datetime.now(timezone.utc) + timedelta(days=1),
            # }
            to_encode = {"sub":str(user["id"])}
            expire = datetime.now(timezone.utc) + timedelta(minutes=1995)
            to_encode.update({"exp": expire})
            encoded_jwt = jwt.encode(
                # payload,
                to_encode,
                secret_key,
                algorithm="HS256"
            )  
            return encoded_jwt
        except Exception as e:
            raise e 
        
class CustomHTTPBearer(HTTPBearer):
    async def __call__(
        self, request: Request
    ) -> Optional[HTTPAuthorizationCredentials]:
        res = await super().__call__(request)

        try:
            payload = jwt.decode(
                res.credentials, secret_key, algorithms=["HS256"]
            )
            user_id = int(payload["sub"])
            user_data = await database.fetch_one(user.select().where(user.c.id == user_id))
            request.state.user = user_data
            return user_data

        except jwt.ExpiredSignatureError:
            raise HTTPException(401, "Token has expired")

        except jwt.InvalidTokenError:
            raise HTTPException(401, "Invalid token")

oauth2_scheme = CustomHTTPBearer()

def is_complainer(request: Request):
    if not request.state.user["role"] == RoleType.complainer:
        raise HTTPException(403, "Forbidden")

def is_approver(request: Request):
    if not request.state.user["role"] == RoleType.approver:
        raise HTTPException(403, "Forbidden")

def is_admin(request: Request):
    if not request.state.user["role"] == RoleType.admin:
        raise HTTPException(403, "Forbidden")

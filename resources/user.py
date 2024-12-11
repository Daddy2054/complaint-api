from typing import Optional
from fastapi import APIRouter
from fastapi import Depends
from managers.auth import is_admin, oauth2_scheme
from managers.user import UserManager

router = APIRouter(tags=["Users"])

@router.get("/users/", dependencies=[Depends(oauth2_scheme), Depends(is_admin)])
async def get_users(email: Optional[str] = None):
    if email:
        return await UserManager.get_user_by_email(email)
    return await UserManager.get_all_users()
    
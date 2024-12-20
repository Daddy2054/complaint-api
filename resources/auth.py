from fastapi import APIRouter

from managers.user import UserManager
from schemas.request.user import UserRegisterIn, UserLoginIn


router = APIRouter(tags=["Auth"])


@router.post("/register/", status_code=201)
async def register(user_data: UserRegisterIn):
    token = await UserManager().register(user_data.model_dump())
    return {"token": token}


@router.post("/login/", status_code=200)
async def login(user_data: UserLoginIn):
    token, role = await UserManager().login(user_data.model_dump())
    return {"token": token, "role": role}

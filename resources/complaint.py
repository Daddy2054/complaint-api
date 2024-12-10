from typing import List
from fastapi import APIRouter, Depends #, Request
from starlette.requests import Request
from managers.auth import CustomHTTPBearer, is_complainer, oauth2_scheme
from managers.complaint import ComplaintManager
from schemas.request.complaint import ComplaintIn
from schemas.response.complaint import ComplaintOut

router = APIRouter(tags=["Complaints"])


@router.get(
    "/complaints/",
    dependencies=[Depends(oauth2_scheme)],
    response_model=List[ComplaintOut],
)
async def get_complaints(request: Request):
    user = request.state.user
    return await ComplaintManager.get_complaints(user)

# request.headers["authorization"]
@router.post(
    "/complaints/", dependencies=[Depends(oauth2_scheme),
                                  Depends(is_complainer)], 
    response_model=ComplaintOut,
)
async def create_complaint(request: Request, complaint: ComplaintIn):
    user = request.state.user
    return await ComplaintManager.create_complaint(complaint.model_dump(),user)

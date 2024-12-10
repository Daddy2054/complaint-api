from models import complaint
from models.enums import RoleType, State
from db import database

class ComplaintManager:
    @staticmethod
    async def get_complaints(user):
        query = complaint.select()
        if user["role"] == RoleType.complainer:
            query = query.where(complaint.c.complainer_id == user["id"])
        elif user["role"] == RoleType.approver:
            query = query.where(complaint.c.status == State.pending)
        return await database.fetch_all(query)
    
    @staticmethod
    async def create_complaint(complaint_data):
        # complaint_data["complainer_id"] = user["id"]
        # complaint_data["status"] = State.pending
        id_ = await database.execute(complaint.insert().values(**complaint_data))
        return await database.fetch_one(complaint.select().where(complaint.c.id == id_))
import asyncclick as click

from managers.user import UserManager
from models.enums import RoleType
from db import database

@click.command("create_super_user")
@click.option("-f", "--first_name", type=str, required=True)
@click.option("-l", "--last_name", type=str, required=True)
@click.option("-e", "--email", type=str, required=True)
@click.option("-p", "--phone", type=str, required=True)
@click.option("-i", "--iban", type=str, required=True)
@click.option("-pa", "--password", type=str, required=True)
async def create_user(
    first_name,
    last_name,
    email,
    phone,
    iban,
    password,
):
    user_data = {
        "first_name": first_name,
        "last_name": last_name,
        "email": email,
        "phone": phone,
        "iban": iban,
        "role": RoleType.admin,
        "password": password,
    }
    await database.connect()
    await UserManager.register(user_data)
    await database.disconnect()


if __name__ == "__main__":
    create_user(
        _anyio_backend="asyncio",
    )

#export PYTHONPATH=./
#python commands/create_super_user.py -f Test -l Admin -e admin@admin.com -p 123456  -i GB8530fosddfjl -pa 123
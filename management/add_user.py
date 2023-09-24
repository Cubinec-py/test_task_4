from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from management.csv_read import read_csv
from user import User


async def user_add(session: AsyncSession):
    data = await CRUD(User, session).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/users.csv")
        await CRUD(User, session).create_from_csv(data_to_insert)

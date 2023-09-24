from sqlalchemy.ext.asyncio import AsyncSession

from credit.models import Credit
from crud.base import CRUD
from management.csv_read import read_csv


async def credit_add(session: AsyncSession):
    data = await CRUD(Credit, session).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/credits.csv")
        await CRUD(Credit, session).create_from_csv(data_to_insert)

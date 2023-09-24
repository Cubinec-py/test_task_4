from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from management.csv_read import read_csv
from plan.models import Plan


async def plan_add(session: AsyncSession):
    data = await CRUD(Plan, session).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/plans.csv")
        await CRUD(Plan, session).create_from_csv(data_to_insert)

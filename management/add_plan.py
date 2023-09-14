from plan.models import Plan
from management.csv_read import read_csv
from crud.base import CRUD


async def plan_add():
    data = await CRUD(Plan).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/plans.csv")
        await CRUD(Plan).create_from_csv(data_to_insert)

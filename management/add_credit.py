from credit.models import Credit
from management.csv_read import read_csv
from crud.base import CRUD


async def credit_add():
    data = await CRUD(Credit).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/credits.csv")
        await CRUD(Credit).create_from_csv(data_to_insert)

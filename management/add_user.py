from user import User
from management.csv_read import read_csv
from crud.base import CRUD


async def user_add():
    data = await CRUD(User).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/users.csv")
        await CRUD(User).create_from_csv(data_to_insert)

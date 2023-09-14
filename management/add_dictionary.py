from dictionary.models import Dictionary
from management.csv_read import read_csv
from crud.base import CRUD


async def dictionary_add():
    data = await CRUD(Dictionary).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/dictionary.csv")
        await CRUD(Dictionary).create_from_csv(data_to_insert)

from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from dictionary.models import Dictionary
from management.csv_read import read_csv


async def dictionary_add(session: AsyncSession):
    data = await CRUD(Dictionary, session).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/dictionary.csv")
        await CRUD(Dictionary, session).create_from_csv(data_to_insert)

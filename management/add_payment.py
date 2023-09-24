from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from management.csv_read import read_csv
from payment.models import Payment


async def payment_add(session: AsyncSession):
    data = await CRUD(Payment, session).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/payments.csv")
        await CRUD(Payment, session).create_from_csv(data_to_insert)

from payment.models import Payment
from management.csv_read import read_csv
from crud.base import CRUD


async def payment_add():
    data = await CRUD(Payment).data_in_db()

    if not bool(data):
        data_to_insert = read_csv("csv_files/payments.csv")
        await CRUD(Payment).create_from_csv(data_to_insert)

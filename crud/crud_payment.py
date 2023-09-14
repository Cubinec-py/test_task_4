import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from payment.models import Payment


class PaymentCRUD(CRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(Payment)
        self.session = session

    async def get_all_by_credit_id(self, credit_id: int):
        query = select(self.model).filter(self.model.credit_id == credit_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_by_date_period(
        self, date_start: datetime.date, date_end: datetime.date
    ):
        query = (
            select(self.model)
            .filter(self.model.payment_date >= date_start)
            .filter(self.model.payment_date <= date_end)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_count_all_by_date_period(
        self, date_start: datetime.date, date_end: datetime.date
    ):
        query = (
            select(func.count(self.model.id))
            .filter(self.model.payment_date >= date_start)
            .filter(self.model.payment_date <= date_end)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_sum_all_by_date_period(
        self, date_start: datetime.date, date_end: datetime.date
    ):
        query = (
            select(func.round(func.sum(self.model.sum), 2))
            .filter(self.model.payment_date >= date_start)
            .filter(self.model.payment_date <= date_end)
        )
        result = await self.session.execute(query)
        return result.scalar()

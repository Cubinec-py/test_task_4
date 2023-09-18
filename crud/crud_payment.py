import datetime

from sqlalchemy import select, func, extract, true
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

    async def get_count_sum_all_by_year(
        self,
        year: int,
    ):
        first_query = (
            select(
                func.round(func.coalesce(func.sum(self.model.sum), 0), 2).label(
                    "year_sum"
                )
            )
            .filter(extract("year", self.model.payment_date) == year)
            .cte()
        )
        query = (
            select(
                [
                    first_query.c.year_sum,
                    func.round(func.coalesce(func.sum(self.model.sum), 0), 2).label(
                        "monthly_sum"
                    ),
                    func.coalesce(func.count(self.model.id), 0),
                ]
            )
            .join(first_query, true())
            .where(extract("year", self.model.payment_date) == year)
            .group_by(extract("month", self.model.payment_date), first_query.c.year_sum)
        )
        result = await self.session.execute(query)
        return result.fetchall()

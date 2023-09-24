import datetime

from sqlalchemy import extract, func, select, true
from sqlalchemy.ext.asyncio import AsyncSession

from credit.models import Credit
from crud.base import CRUD


class CreditCRUD(CRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(Credit)
        self.session = session

    async def get_all_by_user_id(self, user_id: int):
        query = select(self.model).filter(self.model.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_by_date_period(
        self, date_start: datetime.date, date_end: datetime.date
    ):
        query = (
            select(self.model)
            .filter(self.model.issuance_date >= date_start)
            .filter(self.model.issuance_date <= date_end)
        )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_count_all_by_date_period(
        self, date_start: datetime.date, date_end: datetime.date
    ):
        query = (
            select(func.count(self.model.id))
            .filter(self.model.issuance_date >= date_start)
            .filter(self.model.issuance_date <= date_end)
        )
        result = await self.session.execute(query)
        return result.scalar()

    async def get_count_sum_all_by_year(
        self,
        year: int,
    ):
        first_query = (
            select(
                func.round(func.coalesce(func.sum(self.model.body), 0), 2).label(
                    "year_sum"
                )
            )
            .where(extract("year", self.model.issuance_date) == year)
            .cte()
        )
        query = (
            select(
                first_query.c.year_sum,
                func.round(func.coalesce(func.sum(self.model.body), 0), 2).label(
                    "monthly_sum"
                ),
                func.coalesce(func.count(self.model.id), 0),
            )
            .join(first_query, true())
            .where(extract("year", self.model.issuance_date) == year)
            .group_by(
                extract("month", self.model.issuance_date), first_query.c.year_sum
            )
        )
        result = await self.session.execute(query)
        return result.fetchall()

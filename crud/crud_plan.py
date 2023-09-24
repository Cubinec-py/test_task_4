import datetime

from sqlalchemy import extract, func, select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from plan.models import Plan


class PlanCRUD(CRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(Plan)
        self.session = session

    async def exists(self, **kwargs):
        query = select(self.model).filter_by(**kwargs)
        result = await self.session.execute(query)
        return bool(result.scalars().first())

    async def get_plans_by_date(self, insert_date: datetime.date):
        subquery = (
            select(self.model.period)
            .where(self.model.period <= insert_date)
            .where(self.model.period >= insert_date.replace(day=1))
            .order_by(self.model.period.desc())
            .limit(1)
            .scalar_subquery()
        )
        query = select(self.model).where(self.model.period == subquery)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_all_by_year_period(self, insert_year: int):
        first_query = (
            select(
                extract("month", self.model.period).label("month"),
                self.model.category_id,
                func.sum(self.model.sum).label("sum_1"),
            )
            .filter(extract("year", self.model.period) == insert_year)
            .group_by(extract("month", self.model.period), self.model.category_id)
            .order_by(extract("month", self.model.period), self.model.category_id)
            .cte()
        )
        query = select(
            first_query.c.month, func.group_concat(first_query.c.sum_1)
        ).group_by(first_query.c.month)
        result = await self.session.execute(query)
        return result.all()

import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from credit.models import Credit


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

    async def get_sum_all_by_date_period(
        self, date_start: datetime.date, date_end: datetime.date
    ):
        query = (
            select(func.round(func.sum(self.model.body), 2))
            .filter(self.model.issuance_date >= date_start)
            .filter(self.model.issuance_date <= date_end)
        )
        result = await self.session.execute(query)
        return result.scalar()

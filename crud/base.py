from typing import Any

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession

from settings.database import async_session_maker


class CRUD:
    def __init__(self, model, session: AsyncSession | None = None):
        self.model = model
        self.async_session_maker = async_session_maker
        self.session = session

    async def get_by_id(self, pk: int):
        query = select(self.model).filter(self.model.id == pk)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def data_in_db(self):
        query = select(self.model.__table__.columns)
        result = await self.session.execute(query)
        data = result.fetchone()
        return bool(data)

    async def delete_all(self):
        query = self.model.__table__.delete()
        await self.session.execute(query)
        await self.session.commit()
        await self.session.close()

    async def create_from_csv(self, obj_in: list[dict[str, Any]]):
        insert_stmt = insert(self.model).values(obj_in)
        await self.session.execute(insert_stmt)
        await self.session.commit()

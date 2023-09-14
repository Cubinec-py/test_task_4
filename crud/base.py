from typing import Any, Dict, List

from sqlalchemy import select, insert
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
        if not self.session:
            async with self.async_session_maker() as session:
                query = select(self.model.__table__.columns)
                result = await session.execute(query)
                data = result.fetchone()
                return bool(data)
        query = select(self.model.__table__.columns)
        result = await self.session.execute(query)
        data = result.fetchone()
        return bool(data)

    async def delete_all(self):
        query = self.model.__table__.delete()
        await self.session.execute(query)
        await self.session.commit()
        await self.session.close()

    async def create_from_csv(self, obj_in: List[Dict[str, Any]]):
        if not self.session:
            async with self.async_session_maker() as session:
                insert_stmt = insert(self.model).values(obj_in)
                await session.execute(insert_stmt)
                await session.commit()
                await session.close()
            return True
        insert_stmt = insert(self.model).values(obj_in)
        await self.session.execute(insert_stmt)
        await self.session.commit()
        await self.session.close()

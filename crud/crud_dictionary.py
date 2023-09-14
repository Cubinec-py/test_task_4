from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.base import CRUD
from dictionary.models import Dictionary


class DictionaryCRUD(CRUD):
    def __init__(self, session: AsyncSession):
        super().__init__(Dictionary)
        self.session = session

    async def get_dictionary_by_type(self, dictionary_type: str):
        query = select(self.model).filter(self.model.name == dictionary_type)
        result = await self.session.execute(query)
        return result.scalars().first()

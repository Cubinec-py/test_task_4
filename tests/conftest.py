import asyncio
import os
from collections.abc import AsyncGenerator

import pytest
from dotenv import load_dotenv
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import NullPool

from credit.models import *  # noqa
from dictionary.models import *  # noqa
from main import app
from management import credit_add, dictionary_add, payment_add, plan_add, user_add
from payment.models import *  # noqa
from plan.models import *  # noqa
from settings.database import get_async_session, metadata
from user.models import *  # noqa

load_dotenv()

DATABASE_URL_TEST = os.environ.get("TEST_DATABASE_URL")

engine_test = create_async_engine(DATABASE_URL_TEST, poolclass=NullPool)
async_session_maker = sessionmaker(
    bind=engine_test, class_=AsyncSession, expire_on_commit=False
)
metadata.bind = engine_test


async def override_get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


app.dependency_overrides[get_async_session] = override_get_async_session


@pytest.fixture(autouse=True, scope="module")
async def prepare_database():
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    yield
    async with engine_test.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


@pytest.fixture(scope="session")
def event_loop(request):
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="function")
async def db_data_init():
    async with async_session_maker() as session:
        await user_add(session)
        await dictionary_add(session)
        await credit_add(session)
        await plan_add(session)
        await payment_add(session)
        await session.close()


@pytest.fixture(scope="session")
async def client() -> AsyncGenerator[AsyncClient, None]:
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from credit.router import router as credit_router
from management import credit_add, dictionary_add, payment_add, plan_add, user_add
from plan.router import router as plan_router
from settings import Settings, async_session_maker

app = FastAPI(
    title="Test task API",
    description="This project API just for test task",
    version="0.0.1",
    debug=Settings.DEBUG,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=Settings.CORS_ALLOW_ORIGINS,
    allow_credentials=Settings.CORS_ALLOW_CREDENTIALS,
    allow_methods=Settings.CORS_ALLOW_METHODS,
    allow_headers=Settings.CORS_ALLOW_HEADERS,
)


@app.on_event("startup")
async def init_db_data():
    async with async_session_maker() as session:
        await user_add(session)
        await dictionary_add(session)
        await credit_add(session)
        await plan_add(session)
        await payment_add(session)
        await session.close()


API_PREFIX = "/api/v1"
app.include_router(credit_router, prefix=API_PREFIX)
app.include_router(plan_router, prefix=API_PREFIX)

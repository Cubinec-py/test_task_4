from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from settings.database import Settings

from management import user_add, dictionary_add, plan_add, payment_add, credit_add

from credit.router import router as credit_router
from plan.router import router as plan_router


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
    await user_add()
    await dictionary_add()
    await credit_add()
    await plan_add()
    await payment_add()


API_PREFIX = "/api/v1"
app.include_router(credit_router, prefix=API_PREFIX)
app.include_router(plan_router, prefix=API_PREFIX)

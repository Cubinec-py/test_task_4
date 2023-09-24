# This repo just for test task
First, need to create and asset .env file in the root directory.
```dotenv
DATABASE_URL=
```
Activate virtual environment and install dependencies:
```bash
python3 -m venv .venv
source .venv/bin/activate
python3 pip install poetry
poetry install
```
Before start project need to init migrations:
```bash
python3 alembic upgrade head
```
To start project:
```bash
uvicorn app.main:app --port 8000
```
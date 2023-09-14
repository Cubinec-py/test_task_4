from pydantic import BaseModel
from datetime import date


class UserRead(BaseModel):
    id: int
    login: str
    registration_date: date

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class UserCreate(BaseModel):
    id: int
    login: str
    registration_date: date

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

from datetime import date

from pydantic import BaseModel, ConfigDict


class UserRead(BaseModel):
    id: int
    login: str
    registration_date: date

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class UserCreate(BaseModel):
    id: int
    login: str
    registration_date: date

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

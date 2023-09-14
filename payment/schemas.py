from pydantic import BaseModel
from datetime import date


class PaymentRead(BaseModel):
    id: int
    sum: float
    payment_date: date
    credit_id: int
    type_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PaymentCreate(BaseModel):
    id: int
    sum: float
    payment_date: date
    credit_id: int
    type_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

from datetime import date

from pydantic import BaseModel, ConfigDict


class PaymentRead(BaseModel):
    id: int
    sum: float
    payment_date: date
    credit_id: int
    type_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PaymentCreate(BaseModel):
    id: int
    sum: float
    payment_date: date
    credit_id: int
    type_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

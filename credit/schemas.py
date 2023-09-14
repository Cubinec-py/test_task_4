from pydantic import BaseModel
from datetime import date


class CreditCloseRead(BaseModel):
    issuance_date: date
    credit_close: bool = True
    actual_return_date: date
    body: float
    percent: float
    sum_all_payments: float

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class CreditOpenRead(BaseModel):
    issuance_date: date
    credit_close: bool = False
    return_date: date
    credit_overdue_days: int
    body: float
    percent: float
    sum_by_body: float
    sum_by_percent: float

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

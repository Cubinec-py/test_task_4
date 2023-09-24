from datetime import date

from pydantic import BaseModel, ConfigDict


class CreditCloseRead(BaseModel):
    issuance_date: date
    credit_close: bool = True
    actual_return_date: date
    body: float
    percent: float
    sum_all_payments: float

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class CreditOpenRead(BaseModel):
    issuance_date: date
    credit_close: bool = False
    return_date: date
    credit_overdue_days: int
    body: float
    percent: float
    sum_by_body: float
    sum_by_percent: float

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

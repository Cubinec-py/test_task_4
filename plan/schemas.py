from datetime import date, datetime

from fastapi import HTTPException
from pydantic import BaseModel, ConfigDict, field_validator


class Plan(BaseModel):
    period: str | None
    sum: float | None = ""
    category_plan: str | None = "видача/збір"


class PlanExists(BaseModel):
    error: str = "Plan already exists"
    data: Plan

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PlanRead(BaseModel):
    period: date
    sum: float
    category_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PlanSuccess(BaseModel):
    message: str = "Success"


class PlanFileError(BaseModel):
    message: str = "Only Excel files (xlsx) are allowed."


class PlanCreate(BaseModel):
    id: int
    period: date
    sum: float
    category_id: int

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PlanCreditPerformance(BaseModel):
    month: int
    category_name: str = "видача"
    sum: float
    credits_sum: float
    percent: float

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class PlanPaymentPerformance(BaseModel):
    month: int
    category_name: str = "збір"
    sum: float
    payments_sum: float
    percent: float

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class YearPerformance(BaseModel):
    year: int
    month: int
    month_issuance_amount: int
    month_plan_issuance_sum: float
    month_issuance_sum: float
    percent_month_plan_issuance: float
    month_payments_amount: int
    month_plan_payments_sum: float
    month_payments_sum: float
    percent_month_plan_payments: float
    percent_month_issuance_of_year_issuance: float
    percent_month_payments_of_year_payments: float

    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)


class InsertDate(BaseModel):
    date: str | date

    @field_validator("date")
    def validate_date(cls, value):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=422,
                detail="Invalid date format. Please use YYYY-MM-DD format.",
            )
        today = date.today()
        if value > today:
            raise HTTPException(
                status_code=422, detail="Date must be not in the future"
            )
        return value


class InsertYear(BaseModel):
    year: int = 2022

    @field_validator("year")
    def validate_date(cls, value):
        if value < 1000:
            raise HTTPException(
                status_code=404,
                detail="Invalid year format. Please use YYYY format",
            )
        today = date.today().year
        if value > today:
            raise HTTPException(
                status_code=404,
                detail=f"Year must be not in the future, now is {today}",
            )
        return value

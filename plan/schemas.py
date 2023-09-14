from datetime import datetime, date
from pydantic import BaseModel, validator

from fastapi import HTTPException


class Plan(BaseModel):
    period: str | None
    sum: float | None = ""
    category_plan: str | None = "видача/збір"


class PlanDayError(BaseModel):
    error: str = "No date found"
    data: Plan


class PlanSummError(BaseModel):
    error: str = "Sum must be 0 or greater than 0"
    data: Plan


class PlanExists(BaseModel):
    error: str = "Plan already exists"
    data: Plan

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PlanRead(BaseModel):
    period: date
    sum: float
    category_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PlanSuccess(BaseModel):
    message: str = "Success"


class PlanFileError(BaseModel):
    message: str = "Only Excel files (xlsx) are allowed."


class PlanCategoryError(BaseModel):
    message: str = "Category not found"
    data: Plan


class PlanCreate(BaseModel):
    id: int
    period: date
    sum: float
    category_id: int

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class InsertDate(BaseModel):
    date: str = "2022-01-01"

    @validator("date")
    def validate_date(cls, value):
        try:
            value = datetime.strptime(value, "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(
                status_code=404,
                detail="Invalid date format. Please use YYYY-MM-DD format.",
            )
        today = date.today()
        if value > today:
            raise HTTPException(
                status_code=404, detail="Date must be not in the future"
            )
        return value


class InsertYear(BaseModel):
    year: int = 2022

    @validator("year")
    def validate_date(cls, value):
        today = date.today().year
        if value > today:
            raise HTTPException(
                status_code=404, detail="Year must be not in the future"
            )
        return value


class PlanCreditPerformance(BaseModel):
    month: int
    category_name: str = "видача"
    sum: float
    credits_sum: float
    percent: float

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


class PlanPaymentPerformance(BaseModel):
    month: int
    category_name: str = "збір"
    sum: float
    payments_sum: float
    percent: float

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


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

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True

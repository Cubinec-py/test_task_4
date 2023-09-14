from fastapi import APIRouter, UploadFile, File, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, date

from dictionary.models import Dictionary
from management.csv_read import read_xlsx
from crud.crud_plan import PlanCRUD
from crud.base import CRUD
from crud.crud_credit import CreditCRUD
from crud.crud_payment import PaymentCRUD
from crud.crud_dictionary import DictionaryCRUD
from plan.schemas import (
    PlanExists,
    PlanDayError,
    PlanSummError,
    PlanRead,
    PlanFileError,
    PlanSuccess,
    PlanCategoryError,
    InsertDate,
    PlanCreditPerformance,
    PlanPaymentPerformance,
    YearPerformance,
    InsertYear,
)
from plan.models import Plan
from plan.utils import last_day_of_month
from settings.database import get_async_session

router = APIRouter(
    tags=["Plans"],
)


@router.post(
    "/plans_insert/",
    description="Method for uploading plans for a new month",
    responses={
        200: {"model": PlanSuccess},
        404: {
            "model": PlanExists
            | PlanDayError
            | PlanSummError
            | PlanFileError
            | PlanCategoryError
        },
    },
)
async def plans_insert(
    file: UploadFile = File(..., description="Only Excel files are allowed."),
    session: AsyncSession = Depends(get_async_session),
) -> dict | PlanExists | PlanDayError | PlanSummError | PlanRead | PlanFileError | PlanSuccess | PlanCategoryError:
    if not file.filename.endswith(".xlsx" or ".xls" or ".xlsm" or ".xml"):
        raise HTTPException(status_code=404, detail=PlanFileError().dict())
    all_data = read_xlsx(file)
    for data in all_data:
        if not data["period"]:
            raise HTTPException(status_code=404, detail=PlanDayError(data=data).dict())
        if not data["sum"] or data["sum"] < 0:
            raise HTTPException(status_code=404, detail=PlanSummError(data=data).dict())
        if not data["category_plan"]:
            raise HTTPException(
                status_code=404, detail=PlanCategoryError(data=data).dict()
            )
        category = data.pop("category_plan")
        dictionary = await DictionaryCRUD(session).get_dictionary_by_type(category)
        data["category_id"] = dictionary.id
        check = await PlanCRUD(session).exists(
            period=data["period"], category_id=data["category_id"]
        )
        if check:
            data["category_plan"] = category
            raise HTTPException(status_code=404, detail=PlanExists(data=data).dict())
    await CRUD(Plan, session).create_from_csv(all_data)
    return PlanSuccess()


@router.post(
    "/plans_performance/",
    description="Method for obtaining information about the execution of plans for a certain date",
    responses={
        200: {"model": list[PlanPaymentPerformance | PlanCreditPerformance | None]},
    },
)
async def plans_performance(
    insert_date: InsertDate, session: AsyncSession = Depends(get_async_session)
) -> list[PlanPaymentPerformance | PlanCreditPerformance | None]:
    insert_date: str | date = insert_date.date
    plans = await PlanCRUD(session).get_plans_by_date(insert_date)
    result = []
    for data in plans:
        dictionary = await CRUD(Dictionary, session).get_by_id(data.category_id)
        data.category_name = dictionary.name
        data.month = data.period.month
        if data.category_name == "видача":
            credits = await CreditCRUD(session).get_all_by_date_period(
                data.period, insert_date
            )
            data.credits_sum = round(sum([credit.body for credit in credits]), 2)
            data.percent = round(data.credits_sum * 100 / data.sum, 2)
            result.append(PlanCreditPerformance.from_orm(data))
        elif data.category_name == "збір":
            payments = await PaymentCRUD(session).get_all_by_date_period(
                data.period, insert_date
            )
            data.payments_sum = round(sum([credit.sum for credit in payments]), 2)
            data.percent = round(data.payments_sum * 100 / data.sum, 2)
            result.append(PlanPaymentPerformance.from_orm(data))
    return result


@router.post(
    "/year_performance/",
    description="Method for obtaining consolidated information for a given year. Grouping by month.",
    responses={
        200: {"model": list[YearPerformance | None]},
    },
)
async def get_year_performance(
    insert_year: InsertYear, session: AsyncSession = Depends(get_async_session)
) -> list[YearPerformance | None]:
    plans = await PlanCRUD(session).get_all_by_year_period(insert_year.year)
    year = insert_year.year
    result = []
    star_year_date = datetime.strptime(f"{year}-01-01", "%Y-%m-%d")
    end_yaar_date = datetime.strptime(
        f"{year}-12-{last_day_of_month(year, 12)}", "%Y-%m-%d"
    )
    year_issuance_sum = await CreditCRUD(session).get_sum_all_by_date_period(
        star_year_date, end_yaar_date
    )
    year_payments_sum = await PaymentCRUD(session).get_sum_all_by_date_period(
        star_year_date, end_yaar_date
    )

    for plan in plans:
        month = int(plan[0])
        credit_plan, payment_plan = plan[1].split(",")
        star_date = datetime.strptime(f"{year}-{month}-01", "%Y-%m-%d")
        end_date = datetime.strptime(
            f"{year}-{month}-{last_day_of_month(year, month)}", "%Y-%m-%d"
        )

        month_issuance_amount = await CreditCRUD(session).get_count_all_by_date_period(
            star_date, end_date
        )
        month_plan_issuance_sum = float(credit_plan)
        month_issuance_sum = await CreditCRUD(session).get_sum_all_by_date_period(
            star_date, end_date
        )
        percent_month_plan_issuance = round(
            month_issuance_sum * 100 / month_plan_issuance_sum, 2
        )

        month_payments_amount = await PaymentCRUD(session).get_count_all_by_date_period(
            star_date, end_date
        )
        month_plan_payments_sum = float(payment_plan)
        month_payments_sum = await PaymentCRUD(session).get_sum_all_by_date_period(
            star_date, end_date
        )
        percent_month_plan_payments = round(
            month_payments_sum * 100 / month_plan_payments_sum, 2
        )

        percent_month_issuance_of_year_issuance = round(
            month_issuance_sum * 100 / year_issuance_sum, 2
        )
        percent_month_payments_of_year_issuance = round(
            month_payments_sum * 100 / year_payments_sum, 2
        )
        result.append(
            YearPerformance(
                year=year,
                month=month,
                month_issuance_amount=month_issuance_amount,
                month_plan_issuance_sum=month_plan_issuance_sum,
                month_issuance_sum=month_issuance_sum,
                percent_month_plan_issuance=percent_month_plan_issuance,
                month_payments_amount=month_payments_amount,
                month_plan_payments_sum=month_plan_payments_sum,
                month_payments_sum=month_payments_sum,
                percent_month_plan_payments=percent_month_plan_payments,
                percent_month_issuance_of_year_issuance=percent_month_issuance_of_year_issuance,
                percent_month_payments_of_year_payments=percent_month_payments_of_year_issuance,
            )
        )
    return result

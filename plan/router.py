from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlalchemy.ext.asyncio import AsyncSession

from crud import CRUD, CreditCRUD, DictionaryCRUD, PaymentCRUD, PlanCRUD
from dictionary.models import Dictionary
from management.csv_read import read_xlsx
from plan.models import Plan
from plan.schemas import (
    InsertDate,
    InsertYear,
    PlanCreditPerformance,
    PlanExists,
    PlanFileError,
    PlanPaymentPerformance,
    PlanRead,
    PlanSuccess,
    YearPerformance,
)
from settings import get_async_session

router = APIRouter(
    tags=["Plans"],
)


@router.post(
    "/plans_insert/",
    description="Method for uploading plans for a new month",
    responses={
        200: {"model": PlanSuccess},
        404: {"model": PlanExists | PlanFileError},
    },
)
async def plans_insert(
    file: UploadFile = File(..., description="Only Excel files are allowed."),
    session: AsyncSession = Depends(get_async_session),
) -> dict | (PlanExists | (PlanRead | (PlanFileError | PlanSuccess))):
    if not file.filename.endswith(".xlsx" or ".xls" or ".xlsm" or ".xml"):
        raise HTTPException(status_code=404, detail=PlanFileError().dict())
    all_data = await read_xlsx(file)
    for data in all_data:
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


@router.get(
    "/plans_performance/",
    description="Method for obtaining information about the execution of plans for a certain date",
    responses={
        200: {"model": list[PlanPaymentPerformance | (PlanCreditPerformance | None)]},
    },
)
async def plans_performance(
    insert_date: InsertDate = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> list[PlanPaymentPerformance | (PlanCreditPerformance | None)]:
    plans = await PlanCRUD(session).get_plans_by_date(insert_date.date)
    result = []
    for data in plans:
        dictionary = await CRUD(Dictionary, session).get_by_id(data.category_id)
        data.category_name = dictionary.name
        data.month = data.period.month
        if data.category_name == "видача":
            credits = await CreditCRUD(session).get_all_by_date_period(
                data.period, insert_date.date
            )
            data.credits_sum = round(sum([credit.body for credit in credits]), 2)
            data.percent = round(data.credits_sum * 100 / data.sum, 2)
            result.append(PlanCreditPerformance.model_validate(data))
        elif data.category_name == "збір":
            payments = await PaymentCRUD(session).get_all_by_date_period(
                data.period, insert_date.date
            )
            data.payments_sum = round(sum([credit.sum for credit in payments]), 2)
            data.percent = round(data.payments_sum * 100 / data.sum, 2)
            result.append(PlanPaymentPerformance.model_validate(data))
    return result


@router.get(
    "/year_performance/",
    description="Method for obtaining consolidated information for a given year. Grouping by month.",
    responses={
        200: {"model": list[YearPerformance | None]},
    },
)
async def get_year_performance(
    insert_year: InsertYear = Depends(),
    session: AsyncSession = Depends(get_async_session),
) -> list[YearPerformance | None]:
    year = insert_year.year
    plans = await PlanCRUD(session).get_all_by_year_period(year)
    result = []
    issuance_data = await CreditCRUD(session).get_count_sum_all_by_year(year)
    payments_data = await PaymentCRUD(session).get_count_sum_all_by_year(year)

    for num, plan in enumerate(plans):
        month = int(plan[0])
        credit_plan, payment_plan = plan[1].split(",")

        year_issuance_sum, month_issuance_sum, month_issuance_amount = issuance_data[
            num
        ]
        month_plan_issuance_sum = float(credit_plan)
        percent_month_plan_issuance = round(
            month_issuance_sum * 100 / month_plan_issuance_sum, 2
        )

        year_payments_sum, month_payments_sum, month_payments_amount = payments_data[
            num
        ]
        month_plan_payments_sum = float(payment_plan)
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

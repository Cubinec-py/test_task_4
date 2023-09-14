from fastapi import APIRouter, Depends
from typing import List

from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession

from crud.crud_credit import CreditCRUD
from crud.crud_payment import PaymentCRUD
from credit.schemas import CreditCloseRead, CreditOpenRead

from settings.database import get_async_session

router = APIRouter(
    prefix="/user_credits",
    tags=["User credits"],
)


@router.get(
    "/",
    responses={
        200: {"model": List[CreditOpenRead | CreditCloseRead | None]},
    },
    description="Method for obtaining information about the client's loans",
)
async def get_user_credit(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> List[CreditOpenRead | CreditCloseRead | None]:
    user_credits = await CreditCRUD(session).get_all_by_user_id(user_id)
    result = []
    for data in user_credits:
        payments = await PaymentCRUD(session).get_all_by_credit_id(data.id)
        data.credit_close = True if data.actual_return_date else False
        if data.credit_close:
            data.sum_all_payments = round(sum([payment.sum for payment in payments]), 2)
            result.append(CreditCloseRead.from_orm(data))
        else:
            data.credit_overdue_days = (
                datetime.now().date() - payments[-1].payment_date
            ).days
            data.sum_by_body = round(
                sum([payment.sum for payment in payments if payment.type_id == 1]), 2
            )
            data.sum_by_percent = round(
                sum([payment.sum for payment in payments if payment.type_id == 2]), 2
            )
            result.append(CreditOpenRead.from_orm(data))
    return result

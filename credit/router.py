from datetime import datetime

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from credit.schemas import CreditCloseRead, CreditOpenRead
from crud import CreditCRUD, PaymentCRUD
from settings import get_async_session

router = APIRouter(
    prefix="/user_credits",
    tags=["User credits"],
)


@router.get(
    "/{user_id}/",
    responses={
        200: {"model": list[CreditOpenRead | CreditCloseRead | None]},
    },
    description="Method for obtaining information about the client's loans",
)
async def get_user_credit(
    user_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> list[CreditOpenRead | CreditCloseRead | None]:
    user_credits = await CreditCRUD(session).get_all_by_user_id(user_id)
    result = []
    for data in user_credits:
        payments = await PaymentCRUD(session).get_all_by_credit_id(data.id)
        data.credit_close = True if data.actual_return_date else False
        if data.credit_close:
            data.sum_all_payments = round(sum([payment.sum for payment in payments]), 2)
            result.append(CreditCloseRead.model_validate(data))
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
            result.append(CreditOpenRead.model_validate(data))
    return result

from crud.base import CRUD
from crud.crud_credit import CreditCRUD
from crud.crud_dictionary import DictionaryCRUD
from crud.crud_payment import PaymentCRUD
from crud.crud_plan import PlanCRUD

__all__ = (
    "CreditCRUD",
    "DictionaryCRUD",
    "PaymentCRUD",
    "PlanCRUD",
    "CRUD",
)

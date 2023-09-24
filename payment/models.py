from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from settings.database import Base


class Payment(Base):
    __tablename__ = "payment"

    id: Mapped[int] = mapped_column(primary_key=True)
    sum: Mapped[float] = mapped_column(nullable=False)
    payment_date: Mapped[date] = mapped_column(nullable=False)
    credit_id: Mapped[int] = mapped_column(ForeignKey("credit.id", ondelete="CASCADE"))
    type_id: Mapped[int] = mapped_column(
        ForeignKey("dictionary.id", ondelete="CASCADE")
    )

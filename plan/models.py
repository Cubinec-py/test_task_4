from datetime import date

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from settings.database import Base


class Plan(Base):
    __tablename__ = "plan"

    id: Mapped[int] = mapped_column(primary_key=True)
    period: Mapped[date] = mapped_column(nullable=False)
    sum: Mapped[float] = mapped_column(nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("dictionary.id", ondelete="CASCADE")
    )

from datetime import date

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from settings import Base


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    login: Mapped[str] = mapped_column(String(length=50), nullable=False)
    registration_date: Mapped[date] = mapped_column(nullable=False)

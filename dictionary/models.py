from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from settings.database import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(length=50), nullable=False)

from sqlalchemy import Column, Integer, String

from settings.database import Base


class Dictionary(Base):
    __tablename__ = "dictionary"

    id = Column(Integer, primary_key=True)
    name = Column(String(length=50), nullable=False)

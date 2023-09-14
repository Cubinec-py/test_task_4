from sqlalchemy import Column, Integer, String, Date

from settings.database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    login = Column(String(length=50), nullable=False)
    registration_date = Column(Date, nullable=False)

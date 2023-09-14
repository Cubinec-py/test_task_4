from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from settings.database import Base


class Plan(Base):
    __tablename__ = "plan"

    id = Column(Integer, primary_key=True)
    period = Column(Date, nullable=False)
    sum = Column(Float, nullable=False)
    category_id = Column(Integer, ForeignKey("dictionary.id", ondelete="CASCADE"))

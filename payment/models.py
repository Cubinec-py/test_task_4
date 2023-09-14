from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from settings.database import Base


class Payment(Base):
    __tablename__ = "payment"

    id = Column(Integer, primary_key=True)
    sum = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False)
    credit_id = Column(Integer, ForeignKey("credit.id", ondelete="CASCADE"))
    type_id = Column(Integer, ForeignKey("dictionary.id", ondelete="CASCADE"))

from sqlalchemy import Column, Integer, Float, Date, ForeignKey

from settings.database import Base


class Credit(Base):
    __tablename__ = "credit"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    issuance_date = Column(Date, nullable=False)
    return_date = Column(Date, nullable=True)
    actual_return_date = Column(Date, nullable=True)
    body = Column(Float, nullable=False)
    percent = Column(Float, nullable=True)

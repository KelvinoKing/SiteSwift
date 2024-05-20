from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship


class Payment(BaseModel, Base):
    """This class will define the payment model for SITESWIFT"""

    __tablename__ = 'payments'
    order_id = Column(Integer, ForeignKey('order.id'), nullable=False)
    payment_date = Column(DateTime, nullable=False)
    amount = Column(Float, nullable=False)
    payment_method = Column(String(50), nullable=False)  # e.g., 'credit_card', 'paypal'
    order = relationship('Order', backref='payments', cascade='all, delete-orphan', single_parent=True, lazy=True)

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Float, String
from sqlalchemy.orm import relationship


class BillingCycle(BaseModel, Base):
    """This class will define the billing cycle model for SITESWIFT"""

    __tablename__ = 'billing_cycles'
    hosting_plan_id = Column(String(60), ForeignKey('hosting_plan.id'), nullable=False)
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    cycle_start = Column(DateTime, nullable=False)
    cycle_end = Column(DateTime, nullable=False)
    amount_due = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=True)
    orders = relationship('Order', backref='billing_cycle', cascade='all, delete-orphan', single_parent=True, lazy=True)

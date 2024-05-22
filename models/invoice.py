from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey, Float, Boolean
from sqlalchemy.orm import relationship


class Invoice(BaseModel, Base):
    """This class will define the invoice model for SITESWIFT"""

    __tablename__ = 'invoices'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    hosting_plan_id = Column(String(60), ForeignKey('hosting_plan.id'), nullable=False)
    order_id = Column(String(60), ForeignKey('orders.id'), nullable=False)
    amount_due = Column(Float, nullable=False)
    paid = Column(Boolean, default=False)
    order = relationship('Order', backref='invoices', cascade='all, delete-orphan', single_parent=True, lazy=True)

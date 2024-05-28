from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, Float, String
from sqlalchemy.orm import relationship


class Order(BaseModel, Base):
    """This class will define the order model for SITESWIFT"""

    __tablename__ = 'orders'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    hosting_plan_id = Column(String(60), ForeignKey('hosting_plan.id'), nullable=False)
    amount = Column(Float, nullable=False)
    status = Column(String(20), nullable=False)  # e.g., 'pending', 'completed'
    ip_address = Column(String(20), nullable=True)
    user = relationship('User', backref='orders', cascade='all, delete-orphan', single_parent=True, lazy=True)
    hosting_plan = relationship('HostingPlan', backref='orders', cascade='all, delete-orphan', single_parent=True, lazy=True)

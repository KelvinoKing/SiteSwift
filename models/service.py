from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, DateTime, Boolean, String
from sqlalchemy.orm import relationship


class Service(BaseModel, Base):
    """This class will define the service model for SITESWIFT"""

    __tablename__ = 'services'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    hosting_plan_id = Column(String(60), ForeignKey('hosting_plan.id'), nullable=False)
    service_name = Column(String(80), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=True)
    active = Column(Boolean, default=True)
    hosting_plan = relationship('HostingPlan', backref='services', cascade='all, delete-orphan', single_parent=True, lazy=True)

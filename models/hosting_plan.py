from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class HostingPlan(BaseModel, Base):
    """This class will define the hosting plan model for SITESWIFT"""

    __tablename__ = 'hosting_plan'
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    user = relationship('User', backref='hosting_plans', cascade='all, delete-orphan', single_parent=True, lazy=True)

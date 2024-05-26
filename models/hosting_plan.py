from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship


class HostingPlan(BaseModel, Base):
    """This class will define the hosting plan model for SITESWIFT"""

    __tablename__ = 'hosting_plan'
    name = Column(String(80), unique=True, nullable=False)
    description = Column(String(200), nullable=False)
    price = Column(Float, nullable=False)
    max_websites = Column(Integer, nullable=False)
    max_space = Column(Integer, nullable=False)
    max_bandwidth = Column(Integer, nullable=False)
    max_email = Column(Integer, nullable=False)
    max_databases = Column(Integer, nullable=False)

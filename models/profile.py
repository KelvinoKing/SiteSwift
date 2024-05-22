from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, ForeignKey, String
from sqlalchemy.orm import relationship



class Profile(BaseModel, Base):
    """This class will define the profile model for SITESWIFT"""

    __tablename__ = 'profile'
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    full_name = Column(String(120), nullable=True)
    address = Column(String(200), nullable=True)
    phone = Column(String(20), nullable=True)
    profile_pic = Column(String(200), nullable=True)
    # Relationship to user such that when user is deleted then profile is deleted
    # User should have only one profile
    user = relationship('User', backref='profile', cascade='all, delete-orphan', single_parent=True, lazy=True)

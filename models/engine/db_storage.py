import models
from models.base_model import Base
from models.base_model import BaseModel
from models.billing_cycle import BillingCycle
from models.hosting_plan import HostingPlan
from models.invoice import Invoice
from models.order import Order
from models.payment import Payment
from models.profile import Profile
from models.service import Service
from models.user import User
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy import tuple_
from sqlalchemy.orm import Session
from models.admin import Admin


classes = {
    'User': User,
    'Admin': Admin,
    'Profile': Profile,
    'Service': Service,
    'HostingPlan': HostingPlan,
    'BillingCycle': BillingCycle,
    'Order': Order,
    'Invoice': Invoice,
    'Payment': Payment,
    }

load_dotenv()

class DBStorage:
    """interacts with MySQL database"""
    __engine = None
    __session = None
    
    def __init__(self):
        """Instantiates a DBStorage object"""
        SITESWIFT_MYSQL_USER = os.getenv('SITESWIFT_MYSQL_USER')
        SITESWIFT_MYSQL_HOST = os.getenv('SITESWIFT_MYSQL_HOST')
        SITESWIFT_MYSQL_PWD = os.getenv('SITESWIFT_MYSQL_PWD')
        SITESWIFT_MYSQL_DB = os.getenv('SITESWIFT_MYSQL_DB')
        SITESWIFT_ENV = os.getenv('SITESWIFT_ENV')
        SITESWIFT_MYSQL_PORT = os.getenv('SITESWIFT_MYSQL_PORT')
        
        print(f"User: {SITESWIFT_MYSQL_USER}")
        print(f"Host: {SITESWIFT_MYSQL_HOST}")
        print(f"Password: {SITESWIFT_MYSQL_PWD}")
        print(f"Database: {SITESWIFT_MYSQL_DB}")
        print(f"Port: {SITESWIFT_MYSQL_PORT}")
        
        # self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
        #                               format(SITESWIFT_MYSQL_USER,
        #                                      SITESWIFT_MYSQL_PWD,
        #                                      SITESWIFT_MYSQL_HOST,
        #                                      SITESWIFT_MYSQL_DB))
        
        # self.__engine = create_engine(f'mysql+mysqlconnector://{SITESWIFT_MYSQL_USER}:{SITESWIFT_MYSQL_PWD}@{SITESWIFT_MYSQL_HOST}/{SITESWIFT_MYSQL_DB}')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}:{}/{}'.
                                      format(SITESWIFT_MYSQL_USER,
                                             SITESWIFT_MYSQL_PWD,
                                             SITESWIFT_MYSQL_HOST,
                                             SITESWIFT_MYSQL_PORT,
                                             SITESWIFT_MYSQL_DB))
        
        if SITESWIFT_ENV == 'test':
            Base.metadata.drop_all(self.__engine)

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self.__engine)
            self.__session = DBSession()
        return self.__session
            
    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)
    
    
    def get_session(self):
        """Returns the current database session"""
        return self.__session


    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """
        Returns the object based on the class name and its ID, or
        None if not found
        """
        if cls not in classes.values():
            return None

        all_cls = models.storage.all(cls)
        for value in all_cls.values():
            if (value.id == id):
                return value

        return None

    def count(self, cls=None):
        """
        count the number of objects in storage
        """
        all_class = classes.values()

        if not cls:
            count = 0
            for clas in all_class:
                count += len(models.storage.all(clas).values())
        else:
            count = len(models.storage.all(cls).values())

        return count
    
    def add_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> User:
        """Add a new user to the database
        """
        try:
            user = User(first_name=first_name, last_name=last_name, email=email, password_hash=hashed_password)
            self._session.add(user)
            self._session.commit()
            return user
        except Exception as e:
            raise e

        
    def find_user_by(self, **kwargs) -> User:
        """Find a user by a given attribute
        """
        fields, values = [], []
        if not kwargs:
            return None
        for key, value in kwargs.items():
            if hasattr(User, key):
                fields.append(getattr(User, key))
                values.append(value)
            else:
                raise InvalidRequestError
        result = self._session.query(User).filter(tuple_(*fields).
                                                  in_([tuple(values)])).first()
        if result is None:
            raise NoResultFound
        return result

    def update_user(self, user_id: str, **kwargs) -> None:
        """Update a user in the database
        """
        user = self._session.query(User).filter(User.id == user_id).first()
        if user is None:
            return
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
            else:
                raise ValueError
        self._session.commit()

    def add_admin(self, first_name: str, last_name: str, email: str, hashed_password: str) -> Admin:
        """Add a new admin to the database
        """
        try:
            admin = Admin(first_name=first_name, last_name=last_name, email=email, password_hash=hashed_password)
            self._session.add(admin)
            self._session.commit()
            return admin
        except Exception as e:
            raise e
        
    def find_admin_by(self, **kwargs) -> Admin:
        """Find an admin by a given attribute
        """
        fields, values = [], []
        if not kwargs:
            return None
        for key, value in kwargs.items():
            if hasattr(Admin, key):
                fields.append(getattr(Admin, key))
                values.append(value)
            else:
                raise InvalidRequestError
        result = self._session.query(Admin).filter(tuple_(*fields).
                                                  in_([tuple(values)])).first()
        if result is None:
            raise NoResultFound
        return result
    
    def update_admin(self, admin_id: str, **kwargs) -> None:
        """Update an admin in the database
        """
        admin = self._session.query(Admin).filter(Admin.id == admin_id).first()
        if admin is None:
            return
        for key, value in kwargs.items():
            if hasattr(admin, key):
                setattr(admin, key, value)
            else:
                raise ValueError
        self._session.commit()

#!/usr/bin/env python3
"""
In this task you will define a _hash_password method
that takes in a password string arguments and returns bytes.
The returned bytes is a salted hash of the input password,
hashed with bcrypt.hashpw.
The password should be encoded to base64 before hashing.
"""
import bcrypt
from models.engine.db_storage import DBStorage
from models.user import User
from models.admin import Admin
from sqlalchemy.orm.exc import NoResultFound
import uuid


def _hash_password(password: str) -> bytes:
    """
    _hash_password method that takes in a password string arguments
    and returns bytes.
    """
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())


def _generate_uuid() -> str:
    """Generate a random UUID
    """
    return str(uuid.uuid4())


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DBStorage()

    def register_user(self, first_name: str, last_name: str, email: str, password: str) -> User:
        """Register a new user with the database
        """
        try:
            user = self._db.find_user_by(email=email)
            if user:
                raise ValueError("User {} already exists".format(email))
        except NoResultFound:
            hashed_password = _hash_password(password)
            user = self._db.add_user(first_name, last_name, email, hashed_password)
        return user

    def valid_login(self, email: str, password: str) -> bool:
        """Validate a user login
        """
        try:
            user = self._db.find_user_by(email=email)

            if isinstance(password, str):
                password = password.encode('utf-8')
            
            hashed_password = user.password_hash

            if isinstance(hashed_password, str):
                hashed_password = hashed_password.encode('utf-8')
                
            return bcrypt.checkpw(password, hashed_password)
        except NoResultFound:
            return False
        except ValueError:
            return False

    def create_session(self, email: str) -> str:
        """Create a session for the user
        """
        session_id = None
        try:
            user = self._db.find_user_by(email=email)
            session_id = _generate_uuid()
            user.session_id = session_id
            self._db._session.commit()
        except NoResultFound:
            return None
        return session_id

    def get_user_from_session_id(self, session_id: str) -> User:
        """
        Get a user from a session ID
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a session
        """
        if user_id is None:
            return None
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            return None
        return None

    def get_reset_password_token(self, email: str) -> str:
        """Generate a reset token
        """
        user = None
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)
        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """Update a user password
        """
        user = None
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_user(
            user.id,
            hashed_password=hashed_password,
            reset_token=None,
            )
        return None
    
    def update_user(self, user_id: str, **kwargs) -> None:
        """Update a user profile
        """
        user = None
        try:
            user = self._db.find_user_by(id=user_id)
        except NoResultFound:
            user = None
        if user is None:
            raise ValueError
        self._db.update_user(user.id, **kwargs)
        return None
    
    def register_admin(self, first_name: str, last_name: str, email: str, password: str) -> Admin:
        """Register a new admin with the database
        """
        try:
            admin = self._db.find_admin_by(email=email)
            if admin:
                raise ValueError("Admin {} already exists".format(email))
        except NoResultFound:
            hashed_password = password
            admin = self._db.add_admin(first_name, last_name, email, hashed_password)
        return admin
    
    def valid_admin_login(self, email: str, password: str) -> bool:
        """Validate an admin login
        """
        try:
            admin = self._db.find_admin_by(email=email)
            if password != admin.password_hash:
                return False
            return True
        except NoResultFound:
            return False
        except ValueError:
            return False
        
    def create_admin_session(self, email: str) -> str:
        """Create a session for the admin
        """
        session_id = None
        try:
            admin = self._db.find_admin_by(email=email)
            session_id = _generate_uuid()
            admin.session_id = session_id
            self._db._session.commit()
        except NoResultFound:
            return None
        return session_id
    
    def get_admin_from_session_id(self, session_id: str) -> Admin:
        """
        Get an admin from a session ID
        """
        if session_id is None:
            return None
        try:
            admin = self._db.find_admin_by(session_id=session_id)
            return admin
        except NoResultFound:
            return None
        
    def destroy_admin_session(self, admin_id: int) -> None:
        """
        Destroy an admin session
        """
        if admin_id is None:
            return None
        try:
            admin = self._db.find_admin_by(id=admin_id)
            self._db.update_admin(admin.id, session_id=None)
        except NoResultFound:
            return None
        return None
    
    def get_admin_reset_password_token(self, email: str) -> str:
        """Generate a reset token for an admin
        """
        admin = None
        try:
            admin = self._db.find_admin_by(email=email)
        except NoResultFound:
            admin = None
        if admin is None:
            raise ValueError
        reset_token = _generate_uuid()
        self._db.update_admin(admin.id, reset_token=reset_token)
        return reset_token
    
    def update_admin_password(self, reset_token: str, password: str) -> None:
        """Update an admin password
        """
        admin = None
        try:
            admin = self._db.find_admin_by(reset_token=reset_token)
        except NoResultFound:
            admin = None
        if admin is None:
            raise ValueError
        hashed_password = _hash_password(password)
        self._db.update_admin(
            admin.id,
            password_hash=hashed_password,
            reset_token=None,
            )
        return None
    
    def update_admin(self, admin_id: str, **kwargs) -> None:
        """Update an admin profile
        """
        admin = None
        try:
            admin = self._db.find_admin_by(id=admin_id)
        except NoResultFound:
            admin = None
        if admin is None:
            raise ValueError
        self._db.update_admin(admin.id, **kwargs)
        return None

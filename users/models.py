from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    phone = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    password = Column(String, nullable=False) 

    def __init__(self, email, first_name, last_name, phone, password, is_active=True, is_admin=False,):
        self.email = email.lower()
        self.first_name = first_name
        self.last_name = last_name
        self.phone = phone
        self.password = password
        self.is_active = is_active
        self.is_admin = is_admin


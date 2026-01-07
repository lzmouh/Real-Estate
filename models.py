from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True)
    password = Column(String)
    role = Column(String)
    flat = Column(String, nullable=True)

class Property(Base):
    __tablename__ = "properties"
    flat = Column(String, primary_key=True)
    building_name = Column(String)
    building_number = Column(String)
    address = Column(String)
    parking = Column(String)
    internet_line = Column(String)
    internet_provider = Column(String)
    internet_end = Column(Date)
    cost = Column(Float)

class Lease(Base):
    __tablename__ = "leases"
    flat = Column(String, primary_key=True)
    start = Column(Date)
    end = Column(Date)
    rent = Column(Float)
    allowance = Column(Float)

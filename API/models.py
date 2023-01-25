from typing import Optional
from pydantic import BaseModel, Field 
from sqlalchemy import Integer, String, Column, Float, ForeignKey
from sqlalchemy.orm import  relationship
from database import Base
from enum import Enum


class Predictions(Base):
    __tablename__ = "predictions"

    id = Column(Integer, primary_key=True, index=True)
    imagename = Column(String, nullable=False)
    confidence = Column(Float, nullable=False)
    predictedspecy = Column(String, nullable=False)
    presumedspecy = Column(String, nullable=True)
    userid = Column(Integer, ForeignKey('users.id'))
    owner = relationship('Users', back_populates='predictions')



class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, nullable=False)
    hashedpassword = Column(String, nullable=False)
    firstname = Column(String, nullable=True)
    lastname = Column(String, nullable=True)
    predictions = relationship('Predictions', back_populates='owner')

    
class Species(str, Enum):
    specy_1 = "Amanita flavoconia"
    specy_2 = "Amanita muscaria"
    specy_3 = "Baorangia bicolor"
    specy_4 = "Boletus edulis"
    specy_5 = "Coprinus comatus"
    specy_6 = "Galerina marginata"
    specy_7 = "Ganoderma applanatum"
    specy_8 = "Hypholoma fasciculare"
    specy_9 = "Laetiporus sulphureus"
    specy_10 = "Phaeolus schweinitzii"
    specy_11 =  'Pleurotus ostreatus'
    specy_12 = 'Pluteus cervinus'
    specy_13 = 'Psathyrella candolleana'
    specy_14 = 'Psilocybe cyanescens'
    specy_15 = 'Psilocybe zapotecorum'



class CreateUser(BaseModel):
    username: str
    email: str
    password: str
    firstname: Optional[str]
    lastname: Optional[str] 



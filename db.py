import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

DATABASE_URL = "postgresql+psycopg2://postgres:mysecretpassword@localhost:5432/postgres"

engine = sa.create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    user_id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    email = sa.Column(sa.String)
    access_token = sa.Column(sa.String)
    refresh_token = sa.Column(sa.String)
    


class CalendarAuthorization(Base):
    __tablename__ = 'calendar_authorization'
    authorization_id = sa.Column(sa.Integer, primary_key=True)
    provider = sa.Column(sa.String)
    access_token = sa.Column(sa.String)
    refresh_token = sa.Column(sa.String)
    expiry = sa.Column(sa.String)



class Calendar(Base):
    __tablename__ = 'calenar'
    calendar_id = sa.Column(sa.Integer, primary_key=True)
    authorization_id = 
    name = sa.Column(sa.String)
    color = sa.Column(sa.String)
    icon = sa.Column(sa.String)


class Task(Base):
    __tablename__ = 'tasks'
    id = sa.Column(sa.Integer, primary_key=True)
    name = sa.Column(sa.String)
    description = sa.Column(sa.String)
    status = sa.Column(sa.String)
    due_date = sa.Column(sa.String)


class Event(Base):
    __tablename__ = 'events'
    id = sa.Column(sa.Integer, primary_key=True)
    summary = sa.Column(sa.String)
    description = sa.Column(sa.String)
    location = sa.Column(sa.String)
    status = sa.Column(sa.String)
    start_date = sa.Column(sa.String)
    end_date = sa.Column(sa.String)
    attendees = sa.Column(sa.String)
    due_date = sa.Column(sa.String)
    
    

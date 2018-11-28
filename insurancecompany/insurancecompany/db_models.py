import uuid

import datetime
from sqlalchemy import Column, Integer, String, DateTime, Boolean, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL
from sqlalchemy import create_engine, orm


postgres_db = {'drivername': 'postgres',
               'username': 'postgres',
               'password': 'postgres',
               'host': 'localhost',
               'port': 5432,
               'database': 'insurancecompany'}

db_string = URL(**postgres_db)
db = create_engine(db_string)

Session = orm.sessionmaker(bind=db, autoflush=False)
db_session = Session()

Base = declarative_base()


class UserDB(Base):
    __tablename__ = 'users'

    iid = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String)
    password = Column(String)
    role = Column(String)
    additional_metadata = Column(JSON)
    
    def __init__(self, name, email, password, role, additional_metadata):
        self.name = name
        self.email = email
        self.password = password
        self.role = role
        self.additional_metadata = additional_metadata


class SessionDB(Base):
    __tablename__ = 'session'
    session_uid = Column(String, primary_key=True)
    email = Column(String)
    session_start_time = Column(DateTime)
    session_end_time = Column(DateTime)

    def __init__(self, email):
        self.email = email
        self.session_uid = uuid.uuid4()
        self.session_start_time = datetime.datetime.utcnow()
        self.session_end_time = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)


class AppointmentsDB(Base):
    __tablename__ = 'appointments'
    appointment_id = Column(Integer, primary_key=True)
    email_cust = Column(String)
    appointment_request_date = Column(DateTime)
    request_addressed = Column(Boolean)
    request_addressed_details = Column(JSON)

    def __init__(self, email, appointment_request_date, request_addressed, request_addressed_details):
        self.email_cust = email
        self.appointment_request_date = appointment_request_date
        self.request_addressed = request_addressed
        self.request_addressed = request_addressed_details


class InsurancePlanDB(Base):
    __tablename__ = 'insuranceplan'
    plan_id = Column(String, primary_key=True)
    plan_active = Column(Boolean)
    plan_name = Column(String)
    plan_details = Column(JSON)

    def __init__(self, plan_id, plan_active, plan_name, plan_details):
        self.plan_id = plan_id
        self.plan_active = plan_active
        self.plan_name = plan_name
        self.plan_details = plan_details


# if __name__ == "__main__":
#     db_string = URL(**postgres_db)
#     db = create_engine(db_string)
#
#     Base.metadata.create_all(db)

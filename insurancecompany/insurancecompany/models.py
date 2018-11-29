import uuid

from datetime import datetime
from abc import ABC, abstractmethod
from db_models import db, db_session, UserDB, AppointmentsDB, InsurancePlanDB


class User(ABC):
    def __init__(self, username=None, email=None,
                 password=None, phone_no=None,
                 postal_address=None, role=None, session_id=None):
        self.username = username
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.postal_address = postal_address
        self.role = role
        self.session_id = session_id

    @abstractmethod
    def plan_details(self, email, password):
        pass


class Admin(User):
    def __init__(self, username, email, password, phone_no, postal_address):
        super().__init__(username=username, email=email, password=password, phone_no=phone_no,
                         postal_address=postal_address, role='admin', session_id=None)

    def add_user(self, username, email, password, phone_no, postal_address, role, session_id):
        additional_metadata = dict()

        additional_metadata['phone_no'] = phone_no
        additional_metadata['postal_address'] = postal_address
        additional_metadata['session_id'] = session_id

        new_user = UserDB(name=username, email=email, password=password, role=role,
                          additional_metadata=additional_metadata)

        db_session.add(new_user)
        db_session.commit()
        db_session.flush()

        return new_user

    def remove_user(self, email):
        user_to_be_removed = db_session.query(UserDB).filter(UserDB.email == email).one()

        db_session.delete(user_to_be_removed)
        db_session.commit()
        db_session.flush()

    def add_insurance_plan(self, plan_details):
        new_plan = InsurancePlanDB(True, plan_details=plan_details)

        db_session.add(new_plan)
        db_session.commit()
        db_session.flush()

    def remove_insurance_plan(self, plan_id):
        update_plan = db_session.query(InsurancePlanDB).filter(InsurancePlanDB.plan_id == plan_id).one()

        update_plan.plan_active = False

        db_session.update(update_plan)
        db_session.commit()
        db_session.flush()

    def plan_details(self, email, password):
        pass


class SalesRepresentative(User):
    def __init__(self, username, email, password, phone_no, postal_address):
        super().__init__(username=username, email=email, password=password, phone_no=phone_no,
                         postal_address=postal_address, role='salesrep', session_id=None)

    @staticmethod
    def attend_next_customer():
        next_customer = db_session.query(AppointmentsDB).filter(AppointmentsDB.request_addressed is False).one()

        next_customer.request_addressed = True

        db_session.update(next_customer)
        db_session.commit()
        db_session.flush()

    def plan_details(self, email, password):
        pass


class UserProxy(User):
    def __init__(self, customer):
        self._customer = customer
        super().__init__()

    def plan_details(self, email, password):
        if self._customer.email == email and self._customer.password == password:
            user_details = db_session.query(UserDB).filter(UserDB.email == email).one()
            plan_details = eval(user_details.additional_metadata.replace('null', 'None')).get('plan_details', {})
            return plan_details

        else:
            return "Unauthorized Access"


class Customer(User):
    def __init__(self, username, email, password, phone_no, postal_address):
        super().__init__(username=username, email=email, password=password, phone_no=phone_no,
                         postal_address=postal_address, role='customer', session_id=None)

    def buy_plan(self, plan_details):
        curr_customer = db_session.query(UserDB).filter(UserDB.email == self.email).one()

        curr_customer.additional_metadata = eval(curr_customer.additional_metadata.replace('null', 'None'))

        curr_customer.additional_metadata['plan_details'] = plan_details

        db_session.add(curr_customer)
        db_session.commit()
        db_session.flush()

    def request_sales_rep(self):
        email = self.email
        appointment_request_date = datetime.utcnow()
        request_addressed_details = dict()

        appointment = AppointmentsDB(email=email,
                                     appointment_request_date=appointment_request_date,
                                     request_addressed=False,
                                     request_addressed_details=request_addressed_details)

        db_session.add(appointment)
        db_session.commit()
        db_session.flush()

    def plan_details(self, email, password):
        pass


if __name__ == "__main__":
    new_admin = Admin(username='karthik',
                      email='karthik@ic.com',
                      password='idontremember',
                      phone_no='7777777777',
                      postal_address='1, Beverly Park Circle, California')

    new_admin.add_user(username='Sherlock Holmes',
                       email='shelly@ic.com',
                       password='missme',
                       phone_no='2345665432',
                       postal_address='221, Baker Street, London',
                       role='customer',
                       session_id=None)

    # new_admin.remove_user(email='shelly@ic.com')

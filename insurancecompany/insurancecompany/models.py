from db_models import db, db_session, UserDB, AppointmentsDB, InsurancePlanDB


class User:
    def __init__(self, username, email, password, phone_no, postal_address, role, session_id):
        self.username = username
        self.email = email
        self.password = password
        self.phone_no = phone_no
        self.postal_address = postal_address
        self.role = role
        self.session_id = session_id


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


class SalesRepresentative(User):
    def __init__(self, username, email, password, phone_no, postal_address):
        super().__init__(username=username, email=email, password=password, phone_no=phone_no,
                         postal_address=postal_address, role='salesrep', session_id=None)

    @staticmethod
    def attend_next_customer():
        next_customer = db_session.query(AppointmentsDB).filter(AppointmentsDB.request_addressed is False).one()

        # Todo: Retrieve all plans and contact customer logic.

        next_customer.request_addressed = True

        db_session.update(next_customer)
        db_session.commit()
        db_session.flush()


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
                       postal_address='221 Baker Street London',
                       role='customer',
                       session_id=None)

    # new_admin.remove_user(email='shelly@ic.com')
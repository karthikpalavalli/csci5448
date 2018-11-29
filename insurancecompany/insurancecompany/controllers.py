from models import Admin, UserProxy, Customer
from db_models import db, db_session, UserDB, AppointmentsDB, InsurancePlanDB
from insurance_plan import BasicHealthPlan, CancerCare, CardiacCare, BasicLifePlan, ULIPBenefits, ComboPlan


def add_user():
    default_admin = Admin(username='karthik',
                          email='karthik@ic.com',
                          password='idontremember',
                          phone_no='7777777777',
                          postal_address='1, Beverly Park Circle, California')

    username = input("username: ")
    email = input("email: ")
    password = input("password: ")
    phone_no = input("phone no: ")
    postal_address = input("postal address: ")
    role = input("role: ")

    res = default_admin.add_user(username=username,
                                 email=email,
                                 password=password,
                                 phone_no=phone_no,
                                 postal_address=postal_address,
                                 role=role,
                                 session_id=None)

    print('User Added')

    return res


def get_user(email):
    curr_user = db_session.query(UserDB).filter(UserDB.email == email).one()

    username = curr_user.name
    email = curr_user.email
    password = curr_user.password

    mod_additional_metadata = eval(curr_user.additional_metadata.replace('null', 'None'))

    phone_no = mod_additional_metadata.get('phone_no', 'UNK')
    postal_address = mod_additional_metadata.get('postal_address', 'UNK')

    curr_user_obj = Customer(username=username,
                             email=email,
                             password=password,
                             phone_no=phone_no,
                             postal_address=postal_address)

    curr_user_obj.additional_metadata = mod_additional_metadata

    return curr_user_obj


def view_current_plan(curr_user):
    user_proxy = UserProxy(curr_user)

    print("In order to access your profile please enter your credentials.")
    email = input('email: ')
    password = input('password: ')

    res = user_proxy.plan_details(email, password)

    if isinstance(res, str):
        print(res)

    elif isinstance(res, dict):
        if not res:
            print("Currently there are no plans active under your name.")

        for key, value in res.items():
            print(key, ' : ', value)


def buy_plan(curr_user):
    plans_available = ['Basic health plan', 'Basic health plan + cancer care', 'Basic health plan + cardiac care',
                       'Basic life plan', 'Basic life plan + ULIP', 'Combo plan']

    print('Currently the following plans are available for purchase: ')

    for index, plan in enumerate(plans_available):
        print(index+1, '. ', plan)

    choice = int(input('Please enter the choice you wish to buy: '))

    basic_health_plan = BasicHealthPlan()

    add_details = dict()
    add_details['illness_covered'] = ['flu', 'fever', 'headache']
    add_details['co-pay'] = 26.0
    add_details['total-cost'] = 280

    basic_health_plan.add_plan_details(plan_id=choice,
                                       plan_name=plans_available[choice-1],
                                       additional_details=add_details)

    basic_life_plan = BasicLifePlan()

    add_details = dict()
    add_details['pay-term'] = 120
    add_details['vesting-period'] = 40
    add_details['total-cost'] = 240
    add_details['premium-amount'] = 90

    basic_life_plan.add_plan_details(plan_id=choice,
                                     plan_name=plans_available[choice-1],
                                     additional_details=add_details)

    if choice == 1:
        plan_details = basic_health_plan.get_plan_details(choice)

    elif choice == 2:
        cancer_care = CancerCare(basic_health_plan)

        # Modifying already existing object
        cancer_care.add_plan_details(plan_id=choice,
                                     plan_name=plans_available[choice-1],
                                     additional_details=dict())

        plan_details = cancer_care.get_plan_details(choice)

    elif choice == 3:
        cardiac_care = CardiacCare(basic_health_plan)

        # Modifying already existing object
        cardiac_care.add_plan_details(plan_id=choice,
                                      plan_name=plans_available[choice - 1],
                                      additional_details=dict())

        plan_details = cardiac_care.get_plan_details(choice)

    elif choice == 4:
        plan_details = basic_life_plan.get_plan_details(choice)

    elif choice == 5:
        ulip_add_on = ULIPBenefits(basic_life_plan)

        # Modifying already existing object
        ulip_add_on.add_plan_details(plan_id=choice,
                                     plan_name=plans_available[choice - 1],
                                     additional_details=dict())

        plan_details = ulip_add_on.get_plan_details(choice)

    else:
        combo_plan = ComboPlan()

        combo_plan.append(basic_health_plan)
        combo_plan.append(basic_life_plan)

        plan_details = combo_plan.additional_details

    print("Plan successfully bought")

    curr_user.buy_plan(plan_details=plan_details[1])


def schedule_call(curr_user):
    curr_user.request_sales_rep()


if __name__ == "__main__":
    # Add new user
    new_user = add_user()

    # Fetch existing user
    new_user = get_user('leja@ic.com')

    # View current plan for a user
    # view_current_plan(new_user)

    # Customer buys a new plan
    buy_plan(new_user)

    # Schedule a call
    # schedule_call(new_user)

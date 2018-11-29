from abc import ABC, abstractmethod
from copy import deepcopy


class Plan(ABC):
    def __init__(self, plan_type):
        self.plan_type = plan_type
        super().__init__()

    @abstractmethod
    def add_plan_details(self, plan_id, plan_name, additional_details):
        pass

    @abstractmethod
    def get_plan_details(self, plan_id):
        pass


class BasicHealthPlan(Plan):
    def __init__(self, plan_id=None, plan_name=None, additional_details=None):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.additional_details = additional_details
        super().__init__(plan_type='health')

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.additional_details = additional_details

    def get_plan_details(self, plan_id):
        return self.plan_id, self.additional_details


class ExtendedHealthPlan(Plan):
    def __init__(self, plan_to_extend):
        self.plan_to_extend = plan_to_extend
        super().__init__(plan_to_extend.plan_type)

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_to_extend.add_plan_details(plan_id, plan_name, additional_details)

    def get_plan_details(self, plan_id):
        return self.plan_to_extend.get_plan_details(plan_id=plan_id)


class CancerCare(ExtendedHealthPlan):
    def __init__(self, plan_to_extend):
        super().__init__(plan_to_extend=plan_to_extend)

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_to_extend.plan_id = plan_id
        self.plan_to_extend.plan_name = plan_name

        self.plan_to_extend.additional_details['illness_covered'] = self.plan_to_extend.additional_details.\
            get('illness_covered', []) + ['cancer']
        self.plan_to_extend.additional_details['co-pay'] += 16.5
        self.plan_to_extend.additional_details['total-cost'] += 90

    def get_plan_details(self, plan_id):
        return self.plan_to_extend.get_plan_details(plan_id=plan_id)


class CardiacCare(ExtendedHealthPlan):
    def __init__(self, plan_to_extend):
        super().__init__(plan_to_extend=plan_to_extend)

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_to_extend.plan_id = plan_id
        self.plan_to_extend.plan_name = plan_name

        self.plan_to_extend.additional_details['illness_covered'] = self.plan_to_extend.additional_details.\
            get('illness_covered', []) + ['coronary artery disease', 'cardiomyopathy', 'marfan syndrome']
        self.plan_to_extend.additional_details['co-pay'] += 12
        self.plan_to_extend.additional_details['total-cost'] += 80

    def get_plan_details(self, plan_id):
        return self.plan_to_extend.get_plan_details(plan_id=plan_id)


# Adding Life Plans
class BasicLifePlan(Plan):
    def __init__(self, plan_id=None, plan_name=None, additional_details=None):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.additional_details = additional_details
        super().__init__(plan_type='life')

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_id = plan_id
        self.plan_name = plan_name
        self.additional_details = additional_details

    def get_plan_details(self, plan_id):
        return self.plan_id, self.additional_details


class ExtendedLifePlan(Plan):
    def __init__(self, plan_to_extend):
        self.plan_to_extend = plan_to_extend
        super().__init__(plan_to_extend.plan_type)

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_to_extend.add_plan_details(plan_id, plan_name, additional_details)

    def get_plan_details(self, plan_id):
        return self.plan_to_extend.get_plan_details(plan_id=plan_id)


class ULIPBenefits(ExtendedLifePlan):
    def __init__(self, plan_to_extend):
        super().__init__(plan_to_extend=plan_to_extend)

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_to_extend.plan_id = plan_id
        self.plan_to_extend.plan_name = plan_name

        self.plan_to_extend.additional_details['rate-of-return'] = self.plan_to_extend.additional_details.\
            get('rate-of-return', 0.07) * 1.25
        self.plan_to_extend.additional_details['total-cost'] += 40

    def get_plan_details(self, plan_id):
        return self.plan_to_extend.get_plan_details(plan_id=plan_id)


class ComboPlan(Plan):
    def __init__(self):
        self.plans = list()
        self.plan_id = 1
        self.additional_details = dict()
        self.additional_details['total-cost'] = 0
        super().__init__(plan_type='combo')

    def add_plan_details(self, plan_id, plan_name, additional_details):
        self.plan_id = plan_id

    def append_plan(self, new_plan):
        if 'plan_id' not in dir(new_plan):
            new_plan = new_plan.plan_to_extend

        self.plans.append(deepcopy(new_plan))
        self.additional_details['total-cost'] += new_plan.additional_details.get('total-cost', 0) * 0.90

    def get_plan_details(self, plan_id):
        return self.plans, self.additional_details


if __name__ == "__main__":
    bhp = BasicHealthPlan()
    add_details = dict()
    add_details['illness_covered'] = ['flu', 'fever', 'headache']
    add_details['co-pay'] = 26.0
    add_details['total-cost'] = 280
    bhp.add_plan_details(plan_id=2, plan_name='Health plan basic', additional_details=add_details)
    print(bhp.get_plan_details(2))

    ep = CancerCare(bhp)
    ep.add_plan_details(plan_id=3, plan_name='Health plan basic + cancer care', additional_details=dict())
    print(ep.get_plan_details(3))

    lp = BasicLifePlan()
    add_details = dict()
    add_details['pay-term'] = 120
    add_details['vesting-period'] = 40
    add_details['total-cost'] = 240
    add_details['premium-amount'] = 90
    lp.add_plan_details(plan_id=3, plan_name='Life plan basic', additional_details=add_details)

    cp = ComboPlan()
    cp.append_plan(ep)
    cp.append_plan(lp)
    print(cp.plans)
    print(cp.additional_details)
from abc import ABC, abstractmethod


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
        self.plan_to_extend.additional_details['co-pay'] += 10.5

    def get_plan_details(self, plan_id):
        return self.plan_to_extend.get_plan_details(plan_id=plan_id)


if __name__ == "__main__":
    bhp = BasicHealthPlan()
    add_details = dict()
    add_details['illness_covered'] = ['flu', 'fever', 'headache']
    add_details['co-pay'] = 26.0
    bhp.add_plan_details(plan_id=2, plan_name='New plan', additional_details=add_details)
    print(bhp.get_plan_details(2))

    ep = CancerCare(bhp)
    ep.add_plan_details(plan_id=3, plan_name='New plan plus cancer care', additional_details=dict())
    print(ep.get_plan_details(3))

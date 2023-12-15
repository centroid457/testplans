import pathlib
from typing import *


# =====================================================================================================================


# =====================================================================================================================
class TestCaseStep:
    DESCRIPTION: str = None
    details: Dict[str, Any] = {}

    result: Optional[bool] = None

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self) -> bool:
        return True

    def teardown(self):
        pass

    def run(self):
        pass

    def add_details(self, details: Dict[str, Any]):
        pass


# =====================================================================================================================
class TestCase:
    DESCRIPTION: str = None
    details: List[TestCaseStep] = [
        # TCS1
        # TCS2
    ]

    @property
    def result(self):
        for detail in self.details:
            if not detail.result:
                return False
        return True

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self) -> bool:
        return True

    def teardown(self):
        pass

    def run(self):
        for detail in self.details:
            if detail.startup():
                detail.run()
            detail.teardown()


# =====================================================================================================================
class TestPlan:
    DESCRIPTION: str = None
    details: List[TestCase] = [
        # TC1
        # TC2
    ]

    @property
    def result(self):
        for detail in self.details:
            if not detail.result:
                return False
        return True

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self) -> bool:
        return True

    def teardown(self):
        pass

    def run(self):
        for detail in self.details:
            if detail.startup():
                detail.run()
            detail.teardown()


# =====================================================================================================================

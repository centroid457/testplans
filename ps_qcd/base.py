import pathlib
from typing import *


# =====================================================================================================================
class _Base:
    DUT: Any = None
    DESCRIPTION: str = None

    def __init__(self, DUT: Any):
        self.DUT = DUT

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self) -> bool:
        return True

    def teardown(self):
        pass


# =====================================================================================================================
class TestCaseStep(_Base):
    details: Dict[str, Any] = {}
    result: Optional[bool] = None

    def run(self):
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()

    def add_details(self, details: Dict[str, Any]):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================
class TestCase(_Base):
    details: Dict[Type[TestCaseStep], Union[bool, TestCaseStep]] = {
        # TCS1: True
        # TCS2: True
    }

    @property
    def result(self):
        for detail in self.details:
            if not detail.result:
                return False
        return True

    def run(self):
        if self.startup():
            for detail, start in self.details.items():
                self.details[detail] = detail(self.DUT)
                if start:
                    self.details[detail].run()
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class TestPlan(_Base):
    details: Dict[Type[TestCase], Union[bool, TestCase]] = {
        # TC1: True
        # TC2: True
    }

    @property
    def result(self):
        for detail in self.details:
            if not detail.result:
                return False
        return True

    def run(self):
        if self.startup():
            for detail, start in self.details.items():
                self.details[detail] = detail(self.DUT)
                if start:
                    self.details[detail].run()
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================

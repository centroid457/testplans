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
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()

    def add_details(self, details: Dict[str, Any]):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================
class TestCase:
    DESCRIPTION: str = None
    details: Dict[Type[TestCaseStep], bool] = {
        # TCS1: True
        # TCS2: True
    }

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
        if self.startup():
            for detail, start in self.details.items():
                if start:
                    detail().run()
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class TestPlan:
    DESCRIPTION: str = None
    details: Dict[Type[TestCase], bool] = {
        # TC1: True
        # TC2: True
    }

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
        if self.startup():
            for detail, start in self.details.items():
                if start:
                    detail().run()
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================

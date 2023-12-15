import pathlib
from typing import *


# =====================================================================================================================


# =====================================================================================================================
class TestCaseStep:
    DESCRIPTION: str = None
    RESULT: Optional[bool] = None
    DETAILS: Dict[str, Any] = {}

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        pass

    def add_details(self, details: Dict[str, Any]):
        pass


# =====================================================================================================================
class TestCase:
    DESCRIPTION: str = None
    RESULT: Optional[bool] = None
    DETAILS: List[TestCaseStep] = []

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        pass

    def add_details(self, details: Dict[str, Any]):
        pass


# =====================================================================================================================
class ResultTp:
    DESCRIPTION: str = None
    DETAILS: List[TestCase] = []

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self):
        pass

    def teardown(self):
        pass

    def run(self):
        pass

    def add_result(self, tc_result: TestCase):
        pass

    def check_summary_result(self):
        pass


# =====================================================================================================================
class TestPlanBase:
    pass


# =====================================================================================================================

import pathlib
from typing import *


# =====================================================================================================================
class _Base:
    DUT: Any = None
    DESCRIPTION: str = ""
    PROGRESS: int = 0
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    def __init__(self, DUT: Any):
        self.DUT = DUT

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self) -> bool:
        self.PROGRESS = 1
        return True

    def teardown(self):
        self.PROGRESS = 100


# =====================================================================================================================
class TestCaseStep(_Base):
    details: Dict[str, Any] = {}
    result: Optional[bool] = None

    def run(self) -> None:
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()

    def add_details(self, details: Dict[str, Any]) -> None:
        self.details.update(details)

    # -----------------------------------------------------------------------------------------------------------------
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================
class TestCase(_Base):
    details: Dict[Type[TestCaseStep], Union[bool, TestCaseStep]] = {
        # TCS1: True,
        # TCS2: True
    }

    @property
    def result(self) -> bool:
        for detail in self.details.values():
            if detail in [False, None]:
                continue
            if not detail.result:
                return False
        return True

    def run(self) -> None:
        if self.startup():
            for detail, start in self.details.items():
                if start:
                    self.details[detail] = detail(self.DUT)
                    self.details[detail].run()
                    if self.details[detail].STOP_IF_FALSE_RESULT and not self.details[detail].result:
                        break
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class TestPlan(_Base):
    details: Dict[Type[TestCase], Union[bool, TestCase]] = {
        # TC1: True,
        # TC2: True
    }

    @property
    def result(self) -> bool:
        for detail in self.details.values():
            if detail in [False, None]:
                continue
            if not detail.result:
                return False
        return True

    def run(self) -> None:
        if not self.DUT.check_present():
            return

        if self.startup():
            for detail, start in self.details.items():
                if start:
                    self.details[detail] = detail(self.DUT)
                    self.details[detail].run()
                    if self.details[detail].STOP_IF_FALSE_RESULT and not self.details[detail].result:
                        break
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================

import abc
from typing import *

from pyqt_templates import *


# =====================================================================================================================
class _TestCaseBase:
    # just to use in Signals before defining exact
    pass


# =====================================================================================================================
class Signals(SignalsTemplate):
    signal__tc_result_updated = pyqtSignal()
    signal__tc_details_updated = pyqtSignal(_TestCaseBase)


# =====================================================================================================================
class TestCase(_TestCaseBase, abc.ABC):
    # SETTINGS ------------------------------------
    DESCRIPTION: str = ""
    SKIP: Optional[bool] = None     # access only over CLASS attribute! not instance!!!
    PARALLEL: Optional[bool] = True
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    # AUXILIARY -----------------------------------
    SIGNALS: Signals = Signals()

    # VALUES --------------------------------------
    __result: Optional[bool] = None
    details: Dict[str, Any] = None
    progress: int = 0

    DUT: Any = None

    def __init__(self, dut: Any):
        super().__init__()
        self.details = {}
        self.DUT = dut

    @property
    def result(self) -> Optional[bool]:
        return self.__result

    @result.setter
    def result(self, value: Optional[bool]) -> None:
        self.__result = value
        self.SIGNALS.signal__tc_result_updated.emit()

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @classmethod
    def startup_all(cls) -> bool:
        """before batch work
        """
        return True

    def startup(self) -> bool:
        self.progress = 1
        return True

    def teardown(self):
        self.progress = 100

    @classmethod
    def teardown_all(cls):
        pass

    def dump_results(self):
        pass

    def run(self) -> None:
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()

    def clear(self) -> None:
        self.details.clear()
        self.result = None
        # self.SIGNALS.signal__tc_result_updated.emit()

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: Dict[str, Any]) -> None:
        self.details.update(details)
        self.SIGNALS.signal__tc_details_updated.emit(self)

    def details_pretty(self) -> str:
        result = ""
        for name, value in self.details.items():
            result += f"{name}: {value}"
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================

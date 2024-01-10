from typing import *

from PyQt5.QtCore import QThread

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
class TestCase(_TestCaseBase, QThread):
    # SETTINGS ------------------------------------
    DESCRIPTION: str = ""
    SKIP: Optional[bool] = None     # access only over CLASS attribute! not instance!!!
    PARALLEL: Optional[bool] = True
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    # AUXILIARY -----------------------------------
    SIGNALS: Signals = Signals()  # FIXME: need signal ON BASE CLASS! need only one SlotConnection! need Singleton?

    # VALUES --------------------------------------
    DUT: Any = None

    # RESULTS --------------------------------------
    __result: Optional[bool] = None
    details: Dict[str, Any] = None
    exx: Optional[Exception] = None
    progress: int = 0

    def __init__(self, dut: Any):
        super().__init__()
        self.DUT = dut
        self.clear()

    def clear(self) -> None:
        self.__result = None
        self.details = {}
        self.exx = None
        self.progress = 0

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    # STARTUP/TEARDOWN ------------------------------------------------------------------------------------------------
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

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> Optional[bool]:
        return self.__result

    @result.setter
    def result(self, value: Optional[bool]) -> None:
        self.__result = value
        self.SIGNALS.signal__tc_result_updated.emit()

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: Dict[str, Any]) -> None:
        self.details.update(details)
        self.SIGNALS.signal__tc_details_updated.emit(self)

    def details_pretty(self) -> str:
        result = ""
        for name, value in self.details.items():
            result += f"{name}: {value}"
        return result

    # RUN -------------------------------------------------------------------------------------------------------------
    def run(self) -> None:
        # PREPARE --------
        self.clear()
        if not self.DUT.PRESENT:
            return

        # WORK --------
        if self.startup():
            try:
                self.result = self.run_wrapped()
            except Exception as exx:
                self.exx = exx
        self.teardown()

    # REDEFINE --------------------------------------------------------------------------------------------------------
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================

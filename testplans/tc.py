from typing import *

from PyQt5.QtCore import QThread

from pyqt_templates import *


# =====================================================================================================================
class _TestCaseBase:
    # just to use in Signals before defining exact
    pass


# =====================================================================================================================
class Signals(SignalsTemplate):
    signal__tc_finished = pyqtSignal()
    signal__tc_details_updated = pyqtSignal(_TestCaseBase)


# =====================================================================================================================
class TestCaseBase(_TestCaseBase, QThread):
    # SETTINGS ------------------------------------
    DESCRIPTION: str = ""
    SKIP: Optional[bool] = None     # access only over CLASS attribute! not instance!!!
    skip_tc_dut: Optional[bool] = None
    ACYNC: Optional[bool] = True
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    # AUXILIARY -----------------------------------
    signals: Signals = Signals()  # FIXME: need signal ON BASE CLASS! need only one SlotConnection! need Singleton?

    # INSTANCE ------------------------------------
    DUTS_ALL: List[Any]     # applied for CLS!
    DUT: Any

    __result: Optional[bool]
    details: Dict[str, Any]
    exx: Optional[Exception]
    progress: int

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
    def NAME(cls):
        return cls.__name__

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> Optional[bool]:
        return self.__result

    @result.setter
    def result(self, value: Optional[bool]) -> None:
        self.__result = value
        self.signals.signal__tc_finished.emit()

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: Dict[str, Any]) -> None:
        self.details.update(details)
        self.signals.signal__tc_details_updated.emit(self)

    def info_pretty(self) -> str:
        result = ""

        result += f"NAME={self.NAME}\n"
        result += f"DESCRIPTION={self.DESCRIPTION}\n"
        result += f"SKIP={self.SKIP}\n"
        result += f"skip_tc_dut={self.skip_tc_dut}\n"
        result += f"ACYNC={self.ACYNC}\n"
        result += f"result={self.result}\n"
        result += f"progress={self.progress}\n"
        result += f"exx={self.exx}\n"

        result += f"details=====================\n"
        for name, value in self.details.items():
            result += f"{name}: {value}\n"
        return result

    # =================================================================================================================
    @classmethod
    @property
    def TCS_all(cls) -> List['TestCaseBase']:
        result = []
        for dut in cls.DUTS_ALL:
            try:
                tc_dut = dut.TP_RESULTS[cls]
            except:
                tc_dut = cls(dut)
                if not hasattr(dut, "TP_RESULTS"):
                    setattr(dut, "TP_RESULTS", dict())
                dut.TP_RESULTS.update({cls: tc_dut})

            result.append(tc_dut)

        return result

    # =================================================================================================================
    def terminate(self) -> None:
        super().terminate()

        progress = self.progress
        self.teardown()
        self.progress = progress

    @classmethod
    def terminate_all(cls) -> None:
        for tc_dut in cls.TCS_all:
            tc_dut.terminate()

        cls.teardown_all()

    # =================================================================================================================
    def run(self) -> None:
        # PREPARE --------
        self.clear()
        if not self.DUT.PRESENT or self.DUT.SKIP:
            return

        # WORK --------
        if self.startup():
            try:
                self.result = self.run_wrapped()
            except Exception as exx:
                self.exx = exx
        self.teardown()

    @classmethod
    def run_all(cls, duts: List[Any] = None) -> None:
        """run TC on batch duts
        prefered using in thread on upper level!
        """
        # duts = duts or cls.DUTS_ALL or []
        cls.DUTS_ALL = duts

        if not duts:
            return

        if cls.SKIP:
            return

        if not cls.startup_all():
            return

        # BATCH --------------------------
        for tc_dut in cls.TCS_all:
            if tc_dut.skip_tc_dut:
                continue

            tc_dut.start()
            if not cls.ACYNC:
                tc_dut.wait()

        # FINISH --------------------------
        if cls.ACYNC:
            for tc_dut in cls.TCS_all:
                tc_dut.wait()

        cls.teardown_all()

    # REDEFINE ========================================================================================================
    pass

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

    # RUN -------------------------------------------------------------------------------------------------------------
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================
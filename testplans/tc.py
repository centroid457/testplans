import pathlib
from typing import *
import json
from PyQt5.QtCore import QThread

from pyqt_templates import *
from private_values import PrivateJson


# =====================================================================================================================
class _TestCaseBase:
    # just to use in Signals before defining exact
    pass


# class Settings(PrivateJson):
#     value1: int = 0
#     value2: int


# =====================================================================================================================
class Signals(SignalsTemplate):
    signal__tc_state_changed = pyqtSignal(_TestCaseBase)


# =====================================================================================================================
class TestCaseBase(_TestCaseBase, QThread):
    # SETTINGS ------------------------------------
    NAME: str = ""      # set auto!
    DESCRIPTION: str = ""
    SKIP: Optional[bool] = None     # access only over CLASS attribute! not instance!!!
    skip_tc_dut: Optional[bool] = None
    ASYNC: Optional[bool] = True
    # STOP_IF_FALSE_RESULT: Optional[bool] = None     # NOT USED NOW! MAYBE NOT IMPORTANT!!!
    SETTINGS_FILES: Union[None, pathlib.Path, List[pathlib.Path]] = None

    # AUXILIARY -----------------------------------
    signals: Signals = Signals()  # FIXME: need signal ON BASE CLASS! need only one SlotConnection! need Singleton?

    # INSTANCE ------------------------------------
    DUTS: List[Any]     # applied for CLS!
    DUT: Any
    SETTINGS: PrivateJson = None

    __result: Optional[bool]
    details: Dict[str, Any]
    exx: Optional[Exception]
    progress: int

    # DEVICES ------------------------------------
    # device1: DEVICES.dut_example1.Device    # APPLY any if need!

    # def __init__(self, dut: Any, _settings_files: Union[None, pathlib.Path, List[pathlib.Path]] = None):
    def __init__(self, dut: Any):
        super().__init__()
        self.DUT = dut
        self.clear()

        # if _settings_files is not None:
        #     self.SETTINGS_FILES = _settings_files

        self.SETTINGS = PrivateJson(_dict=self.settings_read())

    @classmethod
    def DUTS_input(cls, duts: List[Any]):
        cls.DUTS = duts

    @classmethod
    def settings_read(cls, files: Union[None, pathlib.Path, List[pathlib.Path]] = None) -> dict:
        result = {}

        _settings_files = files or cls.SETTINGS_FILES
        if _settings_files:
            if isinstance(_settings_files, pathlib.Path):
                _settings_files = [_settings_files, ]

            if isinstance(_settings_files, (list, tuple)):
                for file in _settings_files:
                    if file.exists():
                        file_data = json.loads(file.read_text())
                        result.update(file_data)
        return result

    def clear(self) -> None:
        self.__result = None
        self.details = {}
        self.exx = None
        self.progress = 0

    # @classmethod
    # @property
    # def NAME(cls):
    #     return cls.__name__
    #     # return pathlib.Path(__file__).name    # work as last destination where property starts!

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> Optional[bool]:
        return self.__result

    @result.setter
    def result(self, value: Optional[bool]) -> None:
        self.__result = value
        self.signals.signal__tc_state_changed.emit(self)

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: Dict[str, Any]) -> None:
        self.details.update(details)
        self.signals.signal__tc_state_changed.emit(self)

    # =================================================================================================================
    def info_pretty(self) -> str:
        # fixme: ref from info_get
        result = ""

        result += f"NAME={self.NAME}\n"
        result += f"DESCRIPTION={self.DESCRIPTION}\n"
        result += f"SKIP={self.SKIP}\n"
        result += f"skip_tc_dut={self.skip_tc_dut}\n"
        result += f"ASYNC={self.ASYNC}\n"
        result += f"DUT.INDEX={self.DUT.INDEX}\n"
        result += f"result={self.result}\n"
        result += f"progress={self.progress}\n"
        result += f"exx={self.exx}\n"

        result += f"SETTINGS=====================\n"
        if self.SETTINGS:
            for name, value in self.SETTINGS.dict.items():
                result += f"{name}: {value}\n"

        result += f"details=====================\n"
        for name, value in self.details.items():
            result += f"{name}: {value}\n"
        return result

    @classmethod
    def get__info(cls) -> Dict[str, Union[str, None, bool, int, dict, list]]:
        """
        get info/structure about TC
        """
        result = {
            "TC_NAME": cls.NAME,
            "TC_DESCRIPTION": cls.DESCRIPTION,
            "TC_ASYNC": cls.ASYNC,
            "TC_SKIP": cls.SKIP,
            "TC_SETTINGS": cls.settings_read(),
        }
        return result

    # =================================================================================================================
    def get__results(self) -> Dict[str, Any]:
        result = {
            # COORDINATES
            "DUT_INDEX": self.DUT.INDEX,
            "DUT_SKIP": self.DUT.SKIP,
            "DUT_SKIP_TC": self.skip_tc_dut,

            # INFO
            "TC_NAME": self.NAME,
            "TC_DESCRIPTION": self.DESCRIPTION,
            "TC_ASYNC": self.ASYNC,
            "TC_SKIP": self.SKIP,
            "TC_SETTINGS": self.SETTINGS.dict,

            # RESULTS
            "TC_ACTIVE": self.isRunning(),
            "TC_PROGRESS": self.progress,
            "TC_RESULT": self.result,
            "TC_DETAILS": self.details,
        }
        return result

    @classmethod
    def results_get_all(cls) -> List[Dict[str, Any]]:
        results = []
        for tc_dut in cls.TCS_dut_all:
            results.append(tc_dut.get__results())
        return results

    # =================================================================================================================
    @classmethod
    @property
    def TCS_dut_all(cls) -> List['TestCaseBase']:
        """
        get existed tc objects for all DUTs, if not existed - create it in all DUTs
        """
        result = []
        for dut in cls.DUTS:
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
        for tc_dut in cls.TCS_dut_all:
            tc_dut.terminate()

        cls.teardown_all()

    # =================================================================================================================
    def run(self) -> None:
        # PREPARE --------
        self.clear()
        if not self.DUT.present or self.DUT.SKIP:
            return

        # WORK --------
        if self.startup():
            try:
                self.result = self.run_wrapped()
            except Exception as exx:
                self.exx = exx
        self.teardown()

    @classmethod
    def run_all(cls) -> None:
        """run TC on batch duts
        prefered using in thread on upper level!
        """
        if not cls.DUTS:
            return

        if cls.SKIP:
            return

        if not cls.startup_all():
            return

        # BATCH --------------------------
        for tc_dut in cls.TCS_dut_all:
            if tc_dut.skip_tc_dut:
                continue

            tc_dut.start()
            if not cls.ASYNC:
                tc_dut.wait()

        # FINISH --------------------------
        if cls.ASYNC:
            for tc_dut in cls.TCS_dut_all:
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

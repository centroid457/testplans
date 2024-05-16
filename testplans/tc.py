import pathlib
from typing import *
import json
from enum import Enum, auto
from PyQt5.QtCore import QThread

from pyqt_templates import *
from private_values import PrivateJson

# from .devices import DevicesIndexed_WithDut
from .models import *

from logger_aux import Logger
from funcs_aux import NamesIndexed_Base


# =====================================================================================================================
TYPE__RESULT = Union[None, bool, NamesIndexed_Base]


# =====================================================================================================================
class _TestCaseBase0(Logger):
    # just to use in Signals before defining exact
    pass


# class Settings(PrivateJson):
#     value1: int = 0
#     value2: int


# =====================================================================================================================
class Signals(SignalsTemplate):
    signal__tc_state_changed = pyqtSignal(_TestCaseBase0)


# =====================================================================================================================
class _TestCaseBase(_TestCaseBase0, QThread):
    LOG_ENABLE = False
    LOG_USE_FILE = False

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
    TCS__INST: List['TestCaseBase'] = None

    # INSTANCE ------------------------------------
    DEVICES__CLS: Type['DevicesIndexed_WithDut'] = None
    DEVICES__BY_INDEX: 'DevicesIndexed_WithDut' = None

    SETTINGS: PrivateJson = None
    INDEX: int = 0

    result__cls_startup: Optional[bool] = None
    result__cls_teardown: Optional[bool] = None
    __result: Optional[bool]
    __timestamp: float | None = None
    details: Dict[str, Any]
    exx: Optional[Exception]
    progress: int

    # =================================================================================================================
    # def __init__(self, dut: Any, _settings_files: Union[None, pathlib.Path, List[pathlib.Path]] = None):
    def __init__(self, index: int = 0):
        super().__init__()
        self.LOGGER.debug("init tc")

        self.INDEX = index

        if self.DEVICES__CLS:
            self.DEVICES__BY_INDEX = self.DEVICES__CLS(self.INDEX)

        self.clear()

        # if _settings_files is not None:
        #     self.SETTINGS_FILES = _settings_files

        self.SETTINGS = PrivateJson(_dict=self.settings_read())

    @classmethod
    def devices__apply(cls, devices_cls: Type['DevicesIndexed_WithDut'] = None) -> None:
        if devices_cls is not None:
            cls.DEVICES__CLS = devices_cls
        if cls.DEVICES__CLS:
            cls._TCS__INST__generate()

    @classmethod
    def _TCS__INST__generate(cls) -> None:
        """
        create tc objects for all DUTs, if not existed - create it in all DUTs
        """
        cls.TCS__INST = []
        for index in range(cls.DEVICES__CLS.COUNT):
            tc_on_dut = cls(index=index)
            cls.TCS__INST.append(tc_on_dut)

        # FIXME: check if some TC on one base - it would be incorrect!!!???

    # =================================================================================================================
    @property
    def DUT(self) -> Optional['DutBase']:
        """
        this is only for convenience!
        but recommended to use from DEVICES__BY_INDEX! - # TODO: solve it!!!
        """
        return self.DEVICES__BY_INDEX.DUT

    @property
    def timestamp(self) -> float | None:
        """
        None - not even started
        float - was started!
            stable - finished
            UnStable - in progress (active thread)
        """
        if self.__timestamp:
            return self.__timestamp

        if self.isRunning():
            return time.time()

    # =================================================================================================================
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
        self.LOGGER.debug("clear")

        self.__timestamp = None
        self.result = None
        self.details = {}
        self.exx = None
        self.progress = 0

    @classmethod
    def clear__cls(cls):
        cls.result__cls_startup = None
        cls.result__cls_teardown = None
        for tc in cls.TCS__INST:
            tc.clear()

    # @classmethod
    # @property
    # def NAME(cls):
    #     return cls.__name__
    #     # return pathlib.Path(__file__).name    # work as last destination where property starts!

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> TYPE__RESULT:
        return self.__result

    @result.setter
    def result(self, value: TYPE__RESULT) -> None:
        self.__result = value
        self.signals.signal__tc_state_changed.emit(self)

    # # ---------------------------------------------------------
    # @classmethod
    # @property
    # def result__cls_startup(cls) -> Optional[bool]:
    #     return cls.__result__cls_startup
    #
    # @classmethod
    # @result__cls_startup.setter
    # def result__cls_startup(cls, value: Optional[bool]) -> None:
    #     cls.__result__cls_startup = value
    #     # cls.signals.signal__tc_state_changed.emit(cls)

    # DETAILS ---------------------------------------------------------------------------------------------------------
    def details_update(self, details: Dict[str, Any]) -> None:
        self.LOGGER.debug("")

        self.details.update(details)
        # self.signals.signal__tc_state_changed.emit(self)

    # =================================================================================================================
    def terminate(self) -> None:
        self.LOGGER.debug("")

        super().terminate()

        progress = self.progress
        self.teardown()
        self.progress = progress

    @classmethod
    def terminate__cls(cls) -> None:
        for tc_inst in cls.TCS__INST:
            try:
                if tc_inst.isRunning() and not tc_inst.isFinished():
                    tc_inst.terminate()
            except:
                pass

        cls.teardown__cls()

    # =================================================================================================================
    def run(self) -> None:
        self.LOGGER.debug("run")

        # PREPARE --------
        self.clear()
        if not self.DEVICES__BY_INDEX.DUT or not self.DEVICES__BY_INDEX.DUT.connect() or self.DEVICES__BY_INDEX.DUT.SKIP:
            return

        # WORK --------
        self.LOGGER.debug("run-startup")
        if self.startup():
            try:
                self.LOGGER.debug("run-run_wrapped START")
                self.result = self.run__wrapped()
                self.LOGGER.debug(f"run-run_wrapped FINISHED WITH {self.result=}")
            except Exception as exx:
                self.exx = exx
        self.LOGGER.debug("run-teardown")
        self.teardown()

    @classmethod
    def run__cls(cls) -> None:
        """run TC on batch duts(??? may be INDEXES???)
        prefered using in thread on upper level!
        """
        # if not cls.DEVICES__CLS.LIST__DUT:
        #     return

        print(f"run__cls=START={cls.NAME=}={'='*50}")
        if cls.SKIP:
            print(f"run__cls=SKIP={cls.NAME=}={'='*50}")
            return

        # ---------------------------------
        if cls.startup__cls():
            # BATCH --------------------------
            for tc_inst in cls.TCS__INST:
                if tc_inst.skip_tc_dut:
                    continue

                print(f"run__cls=tc_inst.start({tc_inst.INDEX=})")
                tc_inst.start()
                if not cls.ASYNC:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inONEBYONE")
                    tc_inst.wait()

            # WAIT --------------------------
            if cls.ASYNC:
                for tc_inst in cls.TCS__INST:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inPARALLEL")
                    tc_inst.wait()

        # FINISH -------------------------------------------------
        cls.teardown__cls()
        print(f"run__cls=FINISH={cls.NAME=}={'='*50}")

    # STARTUP/TEARDOWN ------------------------------------------------------------------------------------------------
    @classmethod
    def startup__cls(cls) -> TYPE__RESULT:
        """before batch work
        """
        print(f"startup__cls")
        cls.clear__cls()

        result = cls.startup__cls__wrapped()
        print(f"result__cls_startup={result}")
        cls.result__cls_startup = result
        return result

    def startup(self) -> TYPE__RESULT:
        self.LOGGER.debug("")
        self.progress = 1
        return self.startup__wrapped()

    def teardown(self) -> TYPE__RESULT:
        self.LOGGER.debug("")
        self.__timestamp = time.time()
        self.progress = 99
        result = self.teardown__wrapped()
        self.progress = 100
        return result

    @classmethod
    def teardown__cls(cls) -> TYPE__RESULT:
        print(f"run__cls=teardown__cls")
        result = cls.teardown__cls__wrapped()
        if not result:
            print(f"[FAIL] teardown__cls {cls.NAME}")

        cls.result__cls_teardown = result
        return result

    # REDEFINE ========================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT:
        return True

    def startup__wrapped(cls) -> TYPE__RESULT:
        return True

    def run__wrapped(self) -> TYPE__RESULT:
        return True

    def teardown__wrapped(cls) -> TYPE__RESULT:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT:
        return True


# =====================================================================================================================
class Info(_TestCaseBase):
    """
    separated class for gen results/info by models!
    """
    # =================================================================================================================
    def info_pretty(self) -> str:
        self.LOGGER.debug("")

        # fixme: ref from info_get
        result = ""

        result += f"DUT_INDEX={self.INDEX}\n"
        result += f"TC_NAME={self.NAME}\n"
        result += f"TC_DESCRIPTION={self.DESCRIPTION}\n"
        result += f"TC_SKIP={self.SKIP}\n"
        result += f"tc_skip_dut={self.skip_tc_dut}\n"
        result += f"TC_ASYNC={self.ASYNC}\n"
        result += f"tc_result={self.result}\n"
        result += f"tc_progress={self.progress}\n"
        result += f"tc_exx={self.exx}\n"

        result += f"SETTINGS=====================\n"
        if self.SETTINGS:
            for name, value in self.SETTINGS.dict.items():
                result += f"{name}: {value}\n"

        result += f"details=====================\n"
        for name, value in self.details.items():
            result += f"{name}: {value}\n"
        return result

    @classmethod
    def get__info(cls) -> ModelTcInfo:
        """
        get info/structure about TcCls
        """
        result = {
            "TC_NAME": cls.NAME,
            "TC_DESCRIPTION": cls.DESCRIPTION,
            "TC_ASYNC": cls.ASYNC,
            "TC_SKIP": cls.SKIP,
            "TC_SETTINGS": cls.settings_read(),
        }

        return ModelTcInfo(**result)

    # =================================================================================================================
    def get__results(self) -> ModelTcResultFull:
        self.LOGGER.debug("")

        result = {
            **self.get__info().dict(),
            **self.DUT.get__info().dict(),

            # RESULTS
            "tc_timestamp": self.timestamp,
            "tc_active": self.isRunning(),
            "tc_progress": self.progress,
            "tc_result": self.result,
            "tc_details": self.details,
        }
        return ModelTcResultFull(**result)

    @classmethod
    def results__get_all(cls) -> List[Dict[str, Any]]:
        results = []
        for tc_inst in cls.TCS__INST:
            results.append(tc_inst.get__results().dict())
        return results


class TestCaseBase(Info):
    """
    """


# =====================================================================================================================

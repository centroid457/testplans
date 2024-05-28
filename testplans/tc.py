import pathlib
from typing import *
import json
import time
from PyQt5.QtCore import QThread, pyqtSignal

from pyqt_templates import *
from private_values import PrivateJson

from logger_aux import Logger
from funcs_aux import ResultExpect_Base

from .models import *


# =====================================================================================================================
TYPE__RESULT = Union[None, bool, ResultExpect_Base]


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

    DEVICES__BREEDER_CLS: Type['DevicesBreeder'] = None

    # AUXILIARY -----------------------------------
    signals: Signals = Signals()  # FIXME: need signal ON BASE CLASS! need only one SlotConnection! need Singleton?
    TCS__LIST: List['_TestCaseBase'] = []
    _INSTS_DICT_CLS: dict[Any, dict[Any, Any]]

    result__cls_startup: Optional[bool] = None
    result__cls_teardown: Optional[bool] = None

    # INSTANCE ------------------------------------
    _inst_inited: Optional[bool] = None

    INDEX: int
    SETTINGS: PrivateJson
    DEVICES__BREEDER_INST: 'DevicesBreeder'

    _result: Optional[bool] = None
    _timestamp_last: Optional[float]
    timestamp_start: Optional[float]
    details: dict[str, Any]
    exx: Optional[Exception]
    progress: int

    # =================================================================================================================
    @classmethod
    def devices__apply(cls, devices_cls: Type['DevicesBreeder'] = None) -> None:
        if devices_cls is not None:
            cls.DEVICES__BREEDER_CLS = devices_cls
            cls.TCS__LIST = []

        if cls.DEVICES__BREEDER_CLS:
            cls.DEVICES__BREEDER_CLS.generate__objects()
            cls._TCS__LIST__generate()

    @classmethod
    def _TCS__LIST__generate(cls) -> None:
        """
        create tc objects for all DUTs, if not existed - create it in all DUTs
        """
        if cls.TCS__LIST:
            return

        for index in range(cls.DEVICES__BREEDER_CLS.COUNT):
            tc_inst = cls(index=index)
            cls.TCS__LIST.append(tc_inst)

        # FIXME: check if some TC on one base - it would be incorrect!!!???

    # =================================================================================================================
    def __new__(cls, index: int, *args, **kwargs):
        print(f"{cls.__name__}.__NEW__={index=}/{args=}/{kwargs=}")

        if not hasattr(cls, "_INSTS_DICT_CLS"):
            setattr(cls, "_INSTS_DICT_CLS", {})

        if cls not in cls._INSTS_DICT_CLS:
            cls._INSTS_DICT_CLS.update({cls: {}})

        INSTS_DICT = cls._INSTS_DICT_CLS[cls]

        try:
            INST = INSTS_DICT[index]
        except:
            INST = super().__new__(cls)
            INSTS_DICT[index] = INST

        return INST

    def __init__(self, index: int):
        if self._inst_inited:
            return

        # NEW INSTANCE -----------------------------
        self.INDEX = index
        self.clear()
        super().__init__()

        if self.DEVICES__BREEDER_CLS:
            self.DEVICES__BREEDER_INST = self.DEVICES__BREEDER_CLS(index)

        self.SETTINGS = PrivateJson(_dict=self.settings_read())
        self._inst_inited = True

    # =================================================================================================================
    @property
    def timestamp_last(self) -> float | None:
        """
        None - not even started
        float - was started!
            stable - finished
            UnStable - in progress (active thread)
        """
        if self._timestamp_last:
            return self._timestamp_last

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
        self.result = None
        self._timestamp_last = None
        self.timestamp_start = None
        self.details = {}
        self.exx = None
        self.progress = 0

    @classmethod
    def clear__cls(cls):
        cls.result__cls_startup = None
        cls.result__cls_teardown = None
        for tc in cls.TCS__LIST:
            tc.clear()

    # @classmethod
    # @property
    # def NAME(cls):
    #     return cls.__name__
    #     # return pathlib.Path(__file__).name    # work as last destination where property starts!

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> TYPE__RESULT:
        return self._result

    @result.setter
    def result(self, value: TYPE__RESULT) -> None:
        self._result = value
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
        for tc_inst in cls.TCS__LIST:
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
        self.timestamp_start = time.time()
        if not self.DEVICES__BREEDER_INST.DUT or not self.DEVICES__BREEDER_INST.DUT.connect() or self.DEVICES__BREEDER_INST.DUT.SKIP:
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
        # if not cls.DEVICES__BREEDER_CLS.LIST__DUT:
        #     return

        print(f"run__cls=START={cls.NAME=}={'='*50}")
        if cls.SKIP:
            print(f"run__cls=SKIP={cls.NAME=}={'='*50}")
            return

        # ---------------------------------
        if cls.startup__cls():
            # BATCH --------------------------
            for tc_inst in cls.TCS__LIST:
                if tc_inst.skip_tc_dut:
                    continue

                print(f"run__cls=tc_inst.start({tc_inst.INDEX=})")
                tc_inst.start()
                if not cls.ASYNC:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inONEBYONE")
                    tc_inst.wait()

            # WAIT --------------------------
            if cls.ASYNC:
                for tc_inst in cls.TCS__LIST:
                    print(f"run__cls=tc_inst.wait({tc_inst.INDEX=})inPARALLEL")
                    tc_inst.wait()

        # FINISH -------------------------------------------------
        cls.teardown__cls()
        print(f"[TC]FINISH={cls.NAME=}={'='*50}")

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
        self._timestamp_last = time.time()
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
class _Info(_TestCaseBase):
    """
    separated class for gen results/info by models!
    """
    # =================================================================================================================
    def get__info_pretty(self) -> str:
        # fixme: ref from info_get
        result = ""

        result += f"DUT_INDEX={self.INDEX}\n"
        result += f"DUT_SN={self.DEVICES__BREEDER_INST.DUT.SN}\n"
        result += f"TC_NAME={self.NAME}\n"
        result += f"TC_DESCRIPTION={self.DESCRIPTION}\n"
        result += f"TC_SKIP={self.SKIP}\n"
        result += f"tc_skip_dut={self.skip_tc_dut}\n"
        result += f"TC_ASYNC={self.ASYNC}\n"
        result += f"tc_result={self.result}\n"
        result += f"tc_progress={self.progress}\n"
        result += f"tc_exx={self.exx}\n"
        result += f"tc_timestamp_start={self.timestamp_start}\n"
        result += f"tc_timestamp_last={self.timestamp_last}\n"

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
            **self.DEVICES__BREEDER_INST.DUT.get__info().dict(),

            # RESULTS
            "tc_timestamp": self.timestamp_last,
            "tc_active": self.isRunning(),
            "tc_progress": self.progress,
            "tc_result": bool(self.result),
            "tc_details": self.details,
        }
        return ModelTcResultFull(**result)

    @classmethod
    def results__get_all(cls) -> List[Dict[str, Any]]:
        results = []
        for tc_inst in cls.TCS__LIST:
            results.append(tc_inst.get__results().dict())
        return results


class TestCaseBase(_Info):
    """
    """


# =====================================================================================================================

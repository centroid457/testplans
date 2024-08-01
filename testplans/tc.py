import pathlib
from typing import *
import json
import time
from PyQt5.QtCore import QThread, pyqtSignal

from pyqt_templates import *
from private_values import PrivateJson

from logger_aux import Logger
from funcs_aux import *
from .models import *


# =====================================================================================================================
TYPE__RESULT_BASE = Union[bool, Valid, ValidChains] | None
TYPE__RESULT_W_NORETURN = Union[TYPE__RESULT_BASE, NoReturn]
TYPE__RESULT_W_EXX = Union[TYPE__RESULT_BASE, Type[Exception]]


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
    _INSTS_DICT_CLS: dict[Type[Any], dict[Any, Any]]

    result__startup_cls: TYPE__RESULT_BASE = None
    result__teardown_cls: TYPE__RESULT_BASE = None

    result__startup_group: TYPE__RESULT_BASE = None
    result__teardown_group: TYPE__RESULT_BASE = None

    # INSTANCE ------------------------------------
    _inst_inited: Optional[bool] = None

    INDEX: int
    SETTINGS: PrivateJson
    DEVICES__BREEDER_INST: 'DevicesBreeder'

    result__startup: TYPE__RESULT_W_EXX = None
    result__teardown: TYPE__RESULT_W_EXX = None

    _result: TYPE__RESULT_W_EXX = None
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
            cls.TCS__LIST.clear()

        if cls.DEVICES__BREEDER_CLS:
            cls.DEVICES__BREEDER_CLS.generate__objects()
            if not cls.TCS__LIST:
                for index in range(cls.DEVICES__BREEDER_CLS.COUNT):
                    tc_inst = cls(index=index)

    @classmethod
    @property
    def TCS__LIST(cls) -> list[Self]:
        try:
            result = list(_TestCaseBase._INSTS_DICT_CLS[cls].values())
        except:
            result = []
        return result

    # =================================================================================================================
    def __new__(cls, index: int, *args, **kwargs):
        """
        use singletons for every class!
        """
        if not hasattr(_TestCaseBase, "_INSTS_DICT_CLS"):
            setattr(_TestCaseBase, "_INSTS_DICT_CLS", {})

        if cls not in _TestCaseBase._INSTS_DICT_CLS:
            _TestCaseBase._INSTS_DICT_CLS.update({cls: {}})

        INSTS_DICT = _TestCaseBase._INSTS_DICT_CLS[cls]

        try:
            INST = INSTS_DICT[index]
        except:
            INST = super().__new__(cls)
            INSTS_DICT[index] = INST

        print(f"{cls.__name__}.__NEW__={index=}/{args=}/{kwargs=}//groups={len(_TestCaseBase._INSTS_DICT_CLS)}/group={len(INSTS_DICT)}")
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

    @timestamp_last.setter
    def timestamp_last(self, value: float | None) -> None:
        self._timestamp_last = value

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
        self.result__startup = None
        self.result__teardown = None
        self.result = None

        self.timestamp_last = None
        self.timestamp_start = None

        self.details = {}
        self.exx = None
        self.progress = 0

    @classmethod
    def clear__cls(cls):
        cls.result__startup_cls = None
        cls.result__teardown_cls = None
        for tc in cls.TCS__LIST:
            tc.clear()

    @classmethod
    def clear__group(cls):
        # FIXME: need correct exit/terminate group
        cls.result__startup_group = None
        cls.result__teardown_group = None

    # @classmethod
    # @property
    # def NAME(cls):
    #     return cls.__name__
    #     # return pathlib.Path(__file__).name    # work as last destination where property starts!

    # RESULT ----------------------------------------------------------------------------------------------------------
    @property
    def result(self) -> TYPE__RESULT_W_EXX:
        return self._result

    @result.setter
    def result(self, value: TYPE__RESULT_W_EXX) -> None:
        self._result = value
        self.signals.signal__tc_state_changed.emit(self)

    # # ---------------------------------------------------------
    # @classmethod
    # @property
    # def result__startup_cls(cls) -> Optional[bool]:
    #     return cls.__result__cls_startup
    #
    # @classmethod
    # @result__startup_cls.setter
    # def result__startup_cls(cls, value: Optional[bool]) -> None:
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
        if (
                not hasattr(self.DEVICES__BREEDER_INST, "DUT")
                or
                self.DEVICES__BREEDER_INST.DUT.SKIP
                or
                not self.DEVICES__BREEDER_INST.DUT.DEV_FOUND
                or
                not self.DEVICES__BREEDER_INST.DUT.connect()
        ):
            return

        # WORK --------
        self.LOGGER.debug("run-startup")
        if self.startup():
            try:
                self.LOGGER.debug("run-run_wrapped START")
                self.result = self.run__wrapped()
                if isinstance(self.result, Valid):
                    self.result.run__if_not_finished()

                self.LOGGER.debug(f"run-run_wrapped FINISHED WITH {self.result=}")
            except Exception as exx:
                self.result = False
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
    def startup__cls(cls) -> TYPE__RESULT_W_EXX:
        """before batch work
        """
        print(f"startup__cls")
        cls.clear__cls()

        result = cls.startup__cls__wrapped
        result = Valid.get_result_or_exx(result)
        if isinstance(result, Valid):
            result.run__if_not_finished()
        print(f"{cls.result__startup_cls=}")
        cls.result__startup_cls = result
        return result

    def startup(self) -> TYPE__RESULT_W_EXX:
        self.LOGGER.debug("")
        self.progress = 1

        result = self.startup__wrapped
        result = Valid.get_result_or_exx(result)
        if isinstance(result, Valid):
            result.run__if_not_finished()
        self.result__startup = result
        return result

    def teardown(self) -> TYPE__RESULT_W_EXX:
        self.LOGGER.debug("")
        self.timestamp_last = time.time()
        self.progress = 99

        result = self.teardown__wrapped
        result = Valid.get_result_or_exx(result)
        if isinstance(result, Valid):
            result.run__if_not_finished()

        self.progress = 100
        self.result__teardown = result
        return result

    @classmethod
    def teardown__cls(cls) -> TYPE__RESULT_W_EXX:
        print(f"run__cls=teardown__cls")

        result = cls.teardown__cls__wrapped
        result = Valid.get_result_or_exx(result)
        if isinstance(result, Valid):
            result.run__if_not_finished()
        cls.result__teardown_cls = result
        if not result:
            print(f"[FAIL]{cls.result__teardown_cls=}//{cls.NAME}")
        return result

    # REDEFINE ========================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    def startup__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return True

    def run__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return True

    def teardown__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True


# =====================================================================================================================
class _Info(_TestCaseBase):
    """
    separated class for gen results/info by models!
    """
    # =================================================================================================================
    def get__info_pretty(self) -> str:
        # FIXME: GET FROM INFO_GET????
        result = ""

        result += f"DUT_INDEX={self.INDEX}\n"
        result += f"DUT_SN={self.DEVICES__BREEDER_INST.DUT.SN}\n"
        result += f"TC_NAME={self.NAME}\n"
        result += f"TC_DESCRIPTION={self.DESCRIPTION}\n"
        result += f"TC_ASYNC={self.ASYNC}\n"
        result += f"TC_SKIP={self.SKIP}\n"
        result += f"tc_skip_dut={self.skip_tc_dut}\n"

        result += f"SETTINGS=====================\n"
        if self.SETTINGS:
            for name, value in self.SETTINGS.dict.items():
                result += f"{name}: {value}\n"

        result += f"PROGRESS=====================\n"
        result += f"timestamp_start={self.timestamp_start}\n"
        result += f"result__startup={self.result__startup}\n"
        result += f"progress={self.progress}\n"
        result += f"result={self.result}\n"
        result += f"exx={self.exx}\n"
        result += f"result__teardown={self.result__teardown}\n"
        result += f"timestamp_last={self.timestamp_last}\n"

        result += f"DETAILS=====================\n"
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

        try:
            dut_info = self.DEVICES__BREEDER_INST.DUT.get__info().dict()
        except:
            dut_info = {}

        result = {
            **self.get__info().dict(),
            **dut_info,

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

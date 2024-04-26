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


# =====================================================================================================================
class _TestCaseBase(Logger):
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
    TCS__INST: List['TestCaseBase'] = None

    # INSTANCE ------------------------------------
    DEVICES__CLS: Type['DevicesIndexed_WithDut'] = None
    DEVICES__BY_INDEX: 'DevicesIndexed_WithDut' = None

    SETTINGS: PrivateJson = None
    INDEX: int = 0

    result__cls_startup: Optional[bool] = None
    __result: Optional[bool]
    details: Dict[str, Any]
    exx: Optional[Exception]
    progress: int

    # =================================================================================================================
    # def __init__(self, dut: Any, _settings_files: Union[None, pathlib.Path, List[pathlib.Path]] = None):
    def __init__(self, index: int = 0):
        super().__init__()
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
        self.details = {}
        self.exx = None
        self.progress = 0

    @classmethod
    def clear__cls(cls):
        cls.result__cls_startup = None
        # for tc in cls.TCS__INST:
        #     tc.clear()

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
        self.details.update(details)
        # self.signals.signal__tc_state_changed.emit(self)

    # =================================================================================================================
    def info_pretty(self) -> str:
        # fixme: ref from info_get
        result = ""

        result += f"NAME={self.NAME}\n"
        result += f"DESCRIPTION={self.DESCRIPTION}\n"
        result += f"SKIP={self.SKIP}\n"
        result += f"skip_tc_dut={self.skip_tc_dut}\n"
        result += f"ASYNC={self.ASYNC}\n"
        result += f"INDEX={self.INDEX}\n"
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
    def get__info(cls) -> ModelTcClsInfo:
        """
        get info/structure about TcCls
        """
        result = {
            "name": cls.NAME,
            "description": cls.DESCRIPTION,
            "is_async": cls.ASYNC,
            "is_skipped": cls.SKIP,
            "settings": cls.settings_read(),
        }

        return ModelTcClsInfo(**result)

    # =================================================================================================================
    def get__results(self) -> ModelTcInstResult:
        result = {
            **self.get__info().dict(),

            "DEVICE": self.DUT.get__info(),

            # RESULTS
            "is_active": self.isRunning(),
            "is_async": self.ASYNC,
            "is_skipped": self.SKIP,

            "progress": self.progress,
            "result": self.result,
            "details": self.details,
        }
        return ModelTcInstResult(**result)

    @classmethod
    def results_get_all(cls) -> List[Dict[str, Any]]:
        results = []
        for tc_inst in cls.TCS__INST:
            results.append(tc_inst.get__results().dict())
        return results

    # =================================================================================================================
    def terminate(self) -> None:
        super().terminate()

        progress = self.progress
        self.teardown()
        self.progress = progress

    @classmethod
    def terminate__cls(cls) -> None:
        for tc_inst in cls.TCS__INST:
            tc_inst.terminate()

        cls.teardown__cls()

    # =================================================================================================================
    def run(self) -> None:
        # self.LOGGER.debug("run clear")

        # PREPARE --------
        self.clear()
        if not self.DEVICES__BY_INDEX.DUT or not self.DEVICES__BY_INDEX.DUT.connect() or self.DEVICES__BY_INDEX.DUT.SKIP:
            return

        # WORK --------
        # self.LOGGER.debug("run startup")
        if self.startup():
            try:
                # self.LOGGER.debug("run run_wrapped")
                self.result = self.run_wrapped()
                # self.LOGGER.debug(f"{self.result=}")
            except Exception as exx:
                self.exx = exx
        # self.LOGGER.debug("run teardown")
        self.teardown()

    @classmethod
    def run__cls(cls) -> None:
        """run TC on batch duts(??? may be INDEXES???)
        prefered using in thread on upper level!
        """
        # if not cls.DEVICES__CLS.LIST__DUT:
        #     return

        if cls.SKIP:
            return

        # ---------------------------------
        cls.clear__cls()

        cls.result__cls_startup = cls.startup__cls()
        if not cls.result__cls_startup:
            return

        # BATCH --------------------------
        for tc_inst in cls.TCS__INST:
            if tc_inst.skip_tc_dut:
                continue

            tc_inst.start()
            if not cls.ASYNC:
                tc_inst.wait()

        # FINISH --------------------------
        if cls.ASYNC:
            for tc_inst in cls.TCS__INST:
                tc_inst.wait()

        cls.teardown__cls()

    # REDEFINE ========================================================================================================
    pass
    pass
    pass
    pass
    pass
    pass

    # STARTUP/TEARDOWN ------------------------------------------------------------------------------------------------
    @classmethod
    def startup__cls(cls) -> bool:
        """before batch work
        """
        return True

    def startup(self) -> bool:
        self.progress = 1
        return True

    def teardown(self):
        self.progress = 100

    @classmethod
    def teardown__cls(cls):
        pass

    # RUN -------------------------------------------------------------------------------------------------------------
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================

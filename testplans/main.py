# from . import *
from .tc import TestCaseBase
from .devices import DutBase, DeviceBase, DevicesIndexed_WithDut, DevicesIndexed_Example
from .gui import TpGuiBase
from .api import TpApi_Aiohttp, TpApi_FastApi
from .models import *

from typing import *
import json
from pathlib import Path
from PyQt5.QtCore import QThread
from importlib import import_module
import asyncio
from pydantic import BaseModel

from pyqt_templates import *
from server_templates import ServerAiohttpBase, Client_RequestItem, Client_RequestsStack
from object_info import ObjectInfo
from private_values import PrivateJson


# =====================================================================================================================
class Exx__TcsPathNotExists(Exception):
    pass


class Exx__TcItemNotFound(Exception):
    pass


class Exx__TcItemType(Exception):
    pass


class Exx__TcSettingsIncorrect(Exception):
    pass


# =====================================================================================================================
class TpMultyDutBase(QThread):
    signal__tp_start = pyqtSignal()
    signal__tp_stop = pyqtSignal()
    signal__tp_finished = pyqtSignal()

    _signal__tp_reset_duts_sn = pyqtSignal()

    # SETTINGS ------------------------------------------------------
    STAND_ID: Optional[str] = "stand_id__1"
    STAND_TYPE: Optional[str] = "stand_type"
    STAND_DESCRIPTION: Optional[str] = "stand_description"

    API_SERVER__START: bool = True
    API_SERVER__CLS: Type[TpApi_FastApi] = TpApi_FastApi
    api_server: TpApi_FastApi

    GUI__START: bool = True
    GUI__CLS: Type[TpGuiBase] = TpGuiBase

    api_client: Client_RequestsStack = Client_RequestsStack()   # todo: USE CLS!!! + add start

    # DIRPATH_TPS: Union[str, Path] = "TESTPLANS"
    DIRPATH_TCS: Union[str, Path] = "TESTCASES"
    # DIRPATH_DEVS: Union[str, Path] = "DEVICES"
    SETTINGS_BASE_NAME: Union[str, Path] = "SETTINGS_BASE.json"
    SETTINGS_BASE_FILEPATH: Path

    DEVICES__CLS: Type[DevicesIndexed_WithDut] = DevicesIndexed_Example

    # AUX -----------------------------------------------------------
    TCS__CLS: Dict[Union[str, Type[TestCaseBase]], Optional[bool]] = {}     # todo: RENAME TO clss!!!
    # {
    #     Tc1: True,
    #     Tc2: True
    # }

    # DEVICES: List[Union[str, Type[DeviceBase]]]    # settings
    # [
    #     Dev1,
    #     Dev2
    # ]

    tc_active: Optional[Type[TestCaseBase]] = None      # TODO:FIXME: use as PROPERTY!!!! not attribute!
    progress: int = 0   # todo: use as property? by getting from TCS???

    def __init__(self):
        super().__init__()
        # self.DIRPATH_TPS: Path = Path(self.DIRPATH_TPS)
        self.DIRPATH_TCS: Path = Path(self.DIRPATH_TCS)
        # self.DIRPATH_DEVS: Path = Path(self.DIRPATH_DEVS)
        self.SETTINGS_BASE_FILEPATH = self.DIRPATH_TCS.joinpath(self.SETTINGS_BASE_NAME)

        if not self.DIRPATH_TCS.exists():
            msg = f"[ERROR] not found path {self.DIRPATH_TCS.name=}"
            print(msg)
            raise Exx__TcsPathNotExists(msg)

        self.DEVICES__CLS.generate__devices()

        self.tcs__reinit()
        self.slots_connect()

        self.api_server = self.API_SERVER__CLS(data=self)
        if self.API_SERVER__START:
            self.api_server.start()

        self.gui = self.GUI__CLS(self)
        if self.GUI__START:
            # this will BLOCK process
            # this will BLOCK process
            # this will BLOCK process
            # this will BLOCK process
            # this will BLOCK process
            self.gui.run()

    def slots_connect(self) -> None:
        self.signal__tp_start.connect(self.start)
        self.signal__tp_stop.connect(self.terminate)
        self._signal__tp_reset_duts_sn.connect(self.DEVICES__CLS._debug__duts__reset_sn)

        TestCaseBase.signals.signal__tc_state_changed.connect(self.post__tc_results)

    # =================================================================================================================
    def tcs__reinit(self) -> None:
        if not self.TCS__CLS:
            self._tcs__load_from_files()
        self._tcs__apply_classes()
        self._tcs__apply_settings()
        self._tcs__apply_devices()

    def _tcs__load_from_files(self) -> None:
        self.TCS__CLS = {}
        for file in self.DIRPATH_TCS.glob("*.py"):
            if not file.stem.startswith("__"):
                self.TCS__CLS.update({file.stem: True})

    def _tcs__apply_classes(self) -> None:
        result = {}
        for item, using in self.TCS__CLS.items():
            # print(dir(TESTCASES))
            if isinstance(item, str):   # filename
                # tc_cls = import_module(item, "TESTCASES").TestCase    # not working!
                # tc_cls = getattr(TESTCASES, item).TestCase      # not working
                tc_cls = None
                try:
                    tc_cls = import_module(f"{self.DIRPATH_TCS.name}.{item}").TestCase
                except:
                    msg = f"[WARN] no 'TestCase' class in file [{self.DIRPATH_TCS.name}]"
                    print(msg)
                    continue
                if not tc_cls:
                    msg = f"[ERROR] file not found[{item=}] in /{self.DIRPATH_TCS.name}/"
                    raise Exx__TcItemNotFound(msg)
                tc_cls.NAME = item
            elif isinstance(type(item), type) and issubclass(item, TestCaseBase):
                tc_cls = item
                # msg = f"[ERROR] DONT USE IT!"
                # raise Exception(msg)
            else:
                msg = f"[ERROR] type is inconvenient [{item=}]"
                raise Exx__TcItemType(msg)

            tc_cls.SKIP = not using
            result.update({tc_cls: using})

        self.TCS__CLS = result

    def _tcs__apply_settings(self) -> None:
        for tc_cls in self.TCS__CLS:
            tc_cls.SETTINGS_FILES = [self.SETTINGS_BASE_FILEPATH, ]

            settings_tc_filepath = self.DIRPATH_TCS.joinpath(f"{tc_cls.NAME}.json")
            if settings_tc_filepath.exists():
                tc_cls.SETTINGS_FILES.append(settings_tc_filepath)
            else:
                print(f"{settings_tc_filepath=} NOT_EXISTS")
                pass

        # print(f"{tc_cls.SETTINGS=}")

    def _tcs__apply_devices(self) -> None:
        for tc in self.TCS__CLS:
            tc.devices__apply(self.DEVICES__CLS)

    # =================================================================================================================
    def tp__check_active(self) -> bool:
        result = self.tc_active is not None and self.progress not in [0, 100]
        return result

    # =================================================================================================================
    def tp__startup(self) -> bool:
        """
        Overwrite with super! super first!
        """
        self.progress = 1
        return True

    def tp__teardown(self, progress: int = 100) -> None:
        """
        Overwrite with super! super last!
        """
        if self.tc_active:
            self.tc_active.terminate__cls()
        self.tc_active = None

        if progress is None:
            progress = 100
        self.progress = progress

        self.DEVICES__CLS.disconnect__cls()

        self.signal__tp_finished.emit()

    # =================================================================================================================
    def terminate(self) -> None:
        super().terminate()

        # TERMINATE CHILDS!!! ---------------------
        # ObjectInfo(self.currentThread()).print()    # cant find childs!!!

        # finish current ----------------------------
        self.tp__teardown(0)

    def run(self) -> None:
        if self.tp__check_active():
            return

        if not self.tp__startup():
            return

        for step, tc in enumerate(self.TCS__CLS, start=1):
            self.progress = int(step / len(self.TCS__CLS) * 100) - 1
            self.tc_active = tc
            tc.run__cls()

        # FINISH TP ---------------------------------------------------
        self.tp__teardown()

    # =================================================================================================================
    def get__info(self) -> Dict[str, Union[str, None, bool, int, dict, list]]:
        """
        get info/structure about stand/TP
        """
        TP_TCS = []
        for tc in self.TCS__CLS:
            TP_TCS.append(tc.get__info())

        result = {
            # BASE STRING INFO
            "STAND_ID": self.STAND_ID,
            "STAND_TYPE": self.STAND_TYPE,
            "STAND_DESCRIPTION": self.STAND_DESCRIPTION,

            # AUX
            "TP_TCS_COUNT": len(self.TCS__CLS),
            "TP_DUTS_COUNT": self.DEVICES__CLS.COUNT,

            # SETTINGS
            "TP_SETTINGS_BASE": TestCaseBase.settings_read(files=self.SETTINGS_BASE_FILEPATH),

            # STRUCTURE
            "TP_TCS": TP_TCS,
            "TP_DUTS": [],      # TODO: decide how to use
            # [
            #     # [{DUT1}, {DUT2}, …]
            #     {
            #         DUT_ID: 1  # ??? 	# aux
            #         DUT_SKIP: False
            #     }
            # ]

            }
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def get__results(self) -> Dict[str, Union[str, None, bool, int, dict, list]]:
        """
        get all results for stand/TP
        """
        TCS_RESULTS = []
        for tc in self.TCS__CLS:
            TCS_RESULTS.append(tc.results_get_all())

        result = {
            # BASE STRING INFO
            "STAND_ID": self.STAND_ID,
            "STAND_TYPE": self.STAND_TYPE,
            "STAND_DESCRIPTION": self.STAND_DESCRIPTION,

            # TODO: ADD TP SUMMARY RESULT
            # TODO: ADD TP SUMMARY RESULT
            # TODO: ADD TP SUMMARY RESULT
            # TODO: ADD TP SUMMARY RESULT
            # TODO: ADD TP SUMMARY RESULT
            # TODO: ADD TP SUMMARY RESULT

            # SETTINGS
            "TP_SETTINGS_BASE": TestCaseBase.settings_read(files=self.SETTINGS_BASE_FILEPATH),

            # STRUCTURE
            "TCS_RESULTS": TCS_RESULTS,
            }
        return result

    # -----------------------------------------------------------------------------------------------------------------
    def post__tc_results(self, tc_inst: TestCaseBase) -> None:
        body = {
            "STAND_ID": self.STAND_ID,
            "STAND_TYPE": self.STAND_TYPE,
            "STAND_DESCRIPTION": self.STAND_DESCRIPTION,
            **tc_inst.get__results().dict(),
        }
        self.api_client.send(body=body)


# =====================================================================================================================

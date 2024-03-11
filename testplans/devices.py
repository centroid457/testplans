from typing import *
import uuid

from .tc import TestCaseBase


# =====================================================================================================================
class Exx__DevCantAccess(Exception):
    pass


# =====================================================================================================================
class DeviceBase:
    con: Any = None
    present: Optional[bool] = None

    def mark_present(self) -> None:
        self.present = self.check_present()

    def check_present(self) -> bool:
        return True

    def selftest(self) -> Optional[bool]:
        """
        :return: None - not implemented (lets decide it!)
        """
        pass


# =====================================================================================================================
class DutBase(DeviceBase):
    # SETTINGS ------------------------------------
    SKIP: Optional[bool] = None

    # AUX -----------------------------------
    SN: str = None
    TP_RESULTS: Dict[Type[TestCaseBase], TestCaseBase] = None   # dict is very convenient!!!
    INDEX: int = None
    # DUTS: List[Self] = []

    # def __new__(cls, *args, **kwargs):
    #     # FIXME: DECIDE/TRY NOT TO USE IT!!!
    #     instance = super().__new__(cls)
    #     # instance.INDEX = cls.INDEX
    #     # cls.INDEX += 1
    #     instance.INDEX = len(cls.DUTS)
    #     instance.SN = uuid.uuid4().hex
    #     cls.DUTS.append(instance)
    #     return instance

    def __init__(self, index: int):
        self.INDEX = index

    def _reset_sn(self) -> None:
        """this is only for testing middleware"""
        self.SN = uuid.uuid4().hex

    def _SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

    def check_result_final(self) -> Optional[bool]:
        for tc in self.TP_RESULTS.values():
            if tc.SKIP:
                continue
            if not tc.result:
                return tc.result
        return True

    def results_tc_clear(self) -> None:
        for tc in self.TP_RESULTS.values():
            if tc is not None:
                tc.clear()


# =====================================================================================================================
class TpDevicesIndexed:
    """
    object which keep all devices in one place!
    useful for multyDut-like systems.

    If you need just one device for all duts - use direct attribute,
    else use LIST__*NAME* and dont forget to create annotation for direct Indexed item access!

    so you could
    - pass just one instance into all other classes!
    - check all devices for present (or else) in one place!
    - init all and check correctness for all
    """
    # SETTINGS ----------------------
    COUNT: int = 2

    # CLS_LIST__DUT: Callable[[int, ...], DutBase]
    # LIST__DUT: List[DutBase]
    # DUT: DutBase
    #
    # CLS_SINGLE__ATC: Callable[..., DeviceBase]
    # ATC: DeviceBase

    # AUX ----------------------
    _STARTSWITH__CLS_LIST: str = "CLS_LIST__"
    _STARTSWITH__CLS_SINGLE: str = "CLS_SINGLE__"

    _STARTSWITH__DEVICES_LIST: str = "LIST__"

    # instance ---
    INDEX: int = None

    def __init__(self, index: int):
        self.INDEX = index

    def __getattr__(self, item: str) -> DeviceBase:
        devs_attr_name = f"{self._STARTSWITH__DEVICES_LIST}{item}"
        try:
            result = getattr(self, devs_attr_name)[self.INDEX]
        except:
            msg = f"{item=}/{self.INDEX=}"
            print(msg)
            raise Exx__DevCantAccess(msg)

        return result

    @classmethod
    def generate__all(cls) -> None:
        for attr_name in dir(cls):
            if attr_name.startswith(cls._STARTSWITH__CLS_LIST):
                dev_list__name = f"{cls._STARTSWITH__DEVICES_LIST}{attr_name.removeprefix(cls._STARTSWITH__CLS_LIST)}"
                dev_list__value = []
                setattr(cls, dev_list__name, dev_list__value)
                for index in range(cls.COUNT):
                    # FIXME: add Try sentence
                    dev_instance = getattr(cls, attr_name)(index)
                    dev_list__value.append(dev_instance)

            elif attr_name.startswith(cls._STARTSWITH__CLS_SINGLE):
                dev_single__name = attr_name.removeprefix(cls._STARTSWITH__CLS_SINGLE)
                # FIXME: add Try sentence
                dev_instance = getattr(cls, attr_name)()
                setattr(cls, dev_single__name, dev_instance)


# ---------------------------------------------------------------------------------------------------------------------
class DevicesIndexed_Example(TpDevicesIndexed):
    COUNT: int = 2

    CLS_LIST__DUT: Type[DutBase] = DutBase
    LIST__DUT: List[DutBase]
    DUT: DutBase

    CLS_SINGLE__ATC: Type[DeviceBase] = DeviceBase
    ATC: DeviceBase


# =====================================================================================================================

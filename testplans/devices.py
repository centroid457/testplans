from typing import *
import uuid

from .tc import TestCaseBase


# =====================================================================================================================
class Exx__DevCantAccess(Exception):
    pass


# =====================================================================================================================
class DeviceBase:
    con: Any = None
    PRESENT: Optional[bool] = None

    def mark_present(self) -> None:
        self.PRESENT = self.check_present()

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
    TP_RESULTS: Dict[Type[TestCaseBase], TestCaseBase]   # dict is very convenient!!! to find exact tc!!!
    INDEX: int = None

    def __init__(self, index: int = None):
        self.INDEX = index
        self.TP_RESULTS = {}

    def check_result_final(self) -> Optional[bool]:
        for tc in self.TP_RESULTS.values():
            if tc.SKIP:
                continue
            if not tc.result:
                return tc.result
        return True

    def results__clear(self) -> None:
        if not self.TP_RESULTS:
            return
        for tc in self.TP_RESULTS.values():
            if tc is not None:
                tc.clear()

    # DEBUG PURPOSE ---------------------------------------------------------------------------------------------------
    def _debug__reset_sn(self) -> None:
        """this is only for testing middleware"""
        self.SN = uuid.uuid4().hex

    def _bebug__SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)


# =====================================================================================================================
class TpDevicesIndexed:
    """
    object which keep all devices in one place!
    useful for multyDut-like systems.

    If you need just one device for all duts - use direct attribute,
    else use LIST__*NAME* and dont forget to create annotation for direct Indexed item access!

    so you could
    - pass just one instance into all other classes!
    - check all devices for PRESENT (or else) in one place!
    - init all and check correctness for all
    """
    # SETTINGS ----------------------
    COUNT: int = 2

    CLS_LIST__DUT: Type[DutBase] = DutBase
    LIST__DUT: List[DutBase]
    DUT: DutBase

    # CLS_SINGLE__ATC: Callable[..., DeviceBase]
    # ATC: DeviceBase

    # AUX ----------------------
    _STARTSWITH__CLS_LIST: str = "CLS_LIST__"
    _STARTSWITH__CLS_SINGLE: str = "CLS_SINGLE__"

    _STARTSWITH__DEVICES_LIST: str = "LIST__"

    _GROUPS: Dict[str, Union[DeviceBase, List[DeviceBase]]] = {}

    # instance ---
    INDEX: int = None

    def __init__(self, index: int = None):
        self.INDEX = index

    def __getattr__(self, item: str) -> Optional[DeviceBase]:
        if self.INDEX is None:
            return

        devs_attr_name = f"{self._STARTSWITH__DEVICES_LIST}{item}"
        try:
            result = getattr(self, devs_attr_name)[self.INDEX]
        except:
            msg = f"{item=}/{self.INDEX=}"
            print(msg)
            raise Exx__DevCantAccess(msg)

        return result

    @classmethod
    def generate(cls) -> None:
        cls._GROUPS = {}
        for attr_name in dir(cls):
            if attr_name.startswith(cls._STARTSWITH__CLS_LIST):
                group_name = attr_name.removeprefix(cls._STARTSWITH__CLS_LIST)
                dev_list__name = f"{cls._STARTSWITH__DEVICES_LIST}{group_name}"
                dev_list__value = []
                for index in range(cls.COUNT):
                    # FIXME: add Try sentence
                    dev_instance = getattr(cls, attr_name)(index)
                    dev_list__value.append(dev_instance)

                # apply -------
                setattr(cls, dev_list__name, dev_list__value)
                cls._GROUPS.update({group_name: dev_list__value})

            elif attr_name.startswith(cls._STARTSWITH__CLS_SINGLE):
                group_name = attr_name.removeprefix(cls._STARTSWITH__CLS_SINGLE)
                # FIXME: add Try sentence
                dev_instance = getattr(cls, attr_name)()

                # apply -------
                setattr(cls, group_name, dev_instance)
                cls._GROUPS.update({group_name: dev_instance})

    @classmethod
    def mark_present(cls) -> None:
        for group_name, group_value in cls._GROUPS.items():
            if isinstance(group_value, list):
                for device in group_value:
                    device.mark_present()
            else:
                group_value.mark_present()

    @classmethod
    def duts__results_init(cls, tcs: List[Any]) -> None:
        for tc in tcs:
            tc.devices__set(cls())

        for index, dut in enumerate(cls.LIST__DUT):
            dut.TP_RESULTS = dict()
            for tc in tcs:
                dut.TP_RESULTS.update({tc: tc(index)})  # FIXME: try use duts in tc as devices not step by step like here!!!

    @classmethod
    def duts__results_clear(cls) -> None:
        for dut in cls.LIST__DUT:
            dut.results__clear()

    @classmethod
    def _duts__reset_sn(cls) -> None:
        for dut in cls.LIST__DUTS:
            dut._debug__reset_sn()


# ---------------------------------------------------------------------------------------------------------------------
class DevicesIndexed_Example(TpDevicesIndexed):
    COUNT: int = 2

    CLS_SINGLE__ATC: Type[DeviceBase] = DeviceBase
    ATC: DeviceBase


# =====================================================================================================================

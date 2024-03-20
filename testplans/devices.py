from typing import *
import uuid

from .tc import TestCaseBase


# =====================================================================================================================
class Exx__DevCantAccessIndex(Exception):
    pass


class Exx__DevListNotExists(Exception):
    pass


# =====================================================================================================================
class DeviceBase:
    # AUX -----------------------------------
    con: Any = None
    PRESENT: Optional[bool] = None
    INDEX: int = None

    def __init__(self, index: int = None):
        super().__init__()
        self.INDEX = index

    # OVERWRITE =======================================================================================================
    pass
    pass
    pass
    pass

    # CONNECT ---------------------------------
    def connect(self) -> bool:
        return True

    def disconnect(self) -> None:
        return

    # PRESENT ---------------------------------
    def _mark_present(self) -> None:
        self.PRESENT = self.check_present()

    def check_present(self) -> bool:
        return True

    # TESTS -----------------------------------
    def selftest(self) -> Optional[bool]:
        """
        :return: None - not implemented (lets decide it!)
        """
        pass

    # UNIQUE ==========================================================================================================
    pass
    pass
    pass
    pass


# =====================================================================================================================
class DutBase(DeviceBase):
    # SETTINGS ------------------------------------
    SKIP: Optional[bool] = None

    # AUX -----------------------------------
    SN: str = None

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
class DevicesIndexed_Base:
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
    COUNT: int = 1

    # CLS_LIST__DUT: Type[DutBase] = DutBase
    # LIST__DUT: List[DutBase]
    # DUT: DutBase

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
        super().__init__()
        self.INDEX = index
        self.init__devices()

    def __del__(self):
        self.disconnect__cls()

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> Optional[DeviceBase]:
        if self.INDEX is None:
            return

        devs_attr_name = f"{self._STARTSWITH__DEVICES_LIST}{item}"

        # if not hasattr(self, devs_attr_name):     # recursion exx
        if devs_attr_name not in dir(self):
            msg = f"{item=}/{self.INDEX=}"
            print(msg)
            raise Exx__DevListNotExists(msg)
        try:
            result = getattr(self, devs_attr_name)[self.INDEX]
        except:
            msg = f"{item=}/{self.INDEX=}"
            print(msg)
            raise Exx__DevCantAccessIndex(msg)

        return result

    @classmethod
    def check_exists__group__(cls, name: str) -> bool:
        return name in cls._GROUPS

    def check_present__instance__(self, name: str) -> bool:
        result = False
        try:
            device: DeviceBase = getattr(self, name)
            result = device.PRESENT
        except:
            pass
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def init__devices(cls) -> None:
        if not cls._GROUPS:
            cls._generate__cls()
            cls.connect__cls()          # here - run only if not cls._GROUPS!!!
            cls._mark_present__cls()    # here - run only if not cls._GROUPS!!!

    @classmethod
    def _generate__cls(cls) -> None:
        if cls._GROUPS:
            return

        # WORK --------------------------------------
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
    def connect__cls(cls) -> None:
        for group_name, group_value in cls._GROUPS.items():
            devices = []
            if isinstance(group_value, list):
                devices = group_value
            else:
                devices = [group_value, ]

            for device in devices:
                device.connect()

    @classmethod
    def disconnect__cls(cls) -> None:
        for group_name, group_value in cls._GROUPS.items():
            devices = []
            if isinstance(group_value, list):
                devices = group_value
            else:
                devices = [group_value, ]

            for device in devices:
                device.disconnect()

    @classmethod
    def _mark_present__cls(cls) -> None:
        for group_name, group_value in cls._GROUPS.items():
            devices = []
            if isinstance(group_value, list):
                devices = group_value
            else:
                devices = [group_value, ]

            for device in devices:
                device._mark_present()

    # DEBUG PURPOSE ---------------------------------------------------------------------------------------------------
    @classmethod
    def _debug__duts__reset_sn(cls) -> None:
        for dut in cls.LIST__DUT:
            dut._debug__reset_sn()


# =====================================================================================================================
class DevicesIndexed_WithDut(DevicesIndexed_Base):
    CLS_LIST__DUT: Type[DutBase] = DutBase
    LIST__DUT: List[DutBase]
    DUT: DutBase


# =====================================================================================================================
class DevicesIndexed_Example(DevicesIndexed_WithDut):
    COUNT: int = 2

    CLS_SINGLE__ATC: Type[DeviceBase] = DeviceBase
    ATC: DeviceBase


# =====================================================================================================================

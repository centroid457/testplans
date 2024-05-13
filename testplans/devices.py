from typing import *
import uuid

from .tc import TestCaseBase
from .models import *


# =====================================================================================================================
class Exx__DevCantAccessIndex(Exception):
    pass


class Exx__DevNotExists(Exception):
    pass


# =====================================================================================================================
class DeviceBase:
    # AUX -----------------------------------
    conn: Any = None
    INDEX: int = None

    def __init__(self, index: int = None):
        super().__init__()
        self.INDEX = index

    # OVERWRITE =======================================================================================================
    pass
    pass
    pass
    pass

    # AUX -----------------------------------
    NAME: str = None
    DESCRIPTION: str = None
    SN: str = None

    # CONNECT ---------------------------------
    def connect(self) -> bool:
        if self.conn:
            try:
                return self.conn.connect()
            except:
                return False
        return True

    def disconnect(self) -> None:
        try:
            return self.conn.disconnect()
        except:
            pass

    # TESTS -----------------------------------
    def selftest(self) -> Optional[bool]:
        """
        :return: None - not implemented (lets decide it!)
        """
        pass

    def get__info(self) -> ModelDeviceInfo:
        result = {
            "DUT_INDEX": self.INDEX,

            "DUT_NAME": self.NAME or self.__class__.__name__,
            "DUT_DESCRIPTION": self.DESCRIPTION or self.__class__.__name__,
            "DUT_SN": self.SN or "",
        }
        return ModelDeviceInfo(**result)

    # UNIQUE ==========================================================================================================
    pass
    pass
    pass
    pass


# =====================================================================================================================
class DutBase(DeviceBase):
    # SETTINGS ------------------------------------
    SKIP: Optional[bool] = None

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

    def __init__(self, index: int):
        super().__init__()
        self.INDEX = index
        self.generate__devices()

    def __del__(self):
        self.disconnect__cls()

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> Union[DeviceBase, NoReturn]:
        if self.INDEX is None:
            return

        if item in self._GROUPS:
            device = self._GROUPS[item]
            if isinstance(device, list):
                device = device[self.INDEX]
            return device

        else:
            msg = f"{item=}/{self.INDEX=}"
            print(msg)
            raise Exx__DevNotExists(msg)

    @classmethod
    def check_exists__group__(cls, name: str) -> bool:
        return name in cls._GROUPS

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def generate__devices(cls) -> None:
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

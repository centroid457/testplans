from typing import *
import uuid
from enum import Enum, auto

from .tc import TestCaseBase
from .models import *


# =====================================================================================================================
TYPE__BREED_RESULT__ITEM = Union[Any, Exception]
TYPE__BREED_RESULT__GROUP = Union[
    TYPE__BREED_RESULT__ITEM,        # SINGLE variant
    list[TYPE__BREED_RESULT__ITEM]   # LIST variant
]
TYPE__BREED_RESULT__GROUPS = dict[str, TYPE__BREED_RESULT__GROUP]


# =====================================================================================================================
class Exx__DevCantAccessIndex(Exception):
    pass


class Exx__GroupNotExists(Exception):
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
class GroupType(Enum):
    SINGLE = auto()
    LIST = auto()
    NOT_EXISTS = auto()


class ObjectListBreeder_Base:
    """
    class which keep all objects in one place!
    useful for multyObject systems.

    If you need just one device for all duts - use direct attribute,
    else use LIST__*NAME* and dont forget to create annotation for direct Indexed item access!

    so you could
    - pass just one instance into all other classes!
    - check all devices for PRESENT (or else) in one place!
    - init all and check correctness for all

    AFTER GENERATING OBJECTS - ACCESS TO OBJECTS LIST USED OVER THE CLASS!!!
        OBJS_CLS = ObjectListBreeder_Base
        OBJS = OBJS_CLS()
        devs = OBJS_CLS.LIST__DEV
    """
    # SETTINGS ----------------------
    COUNT: int = 1

    # CLS_LIST__DUT: Type[DutBase] = DutBase
    # LIST__DUT: List[DutBase]
    # DUT: DutBase

    # CLS_SINGLE__ATC: Callable[..., DeviceBase]
    # ATC: DeviceBase

    # AUX ----------------------------------------------------------
    # definitions -----
    _STARTSWITH__DEFINE__CLS_LIST: str = "CLS_LIST__"
    _STARTSWITH__DEFINE__CLS_SINGLE: str = "CLS_SINGLE__"

    # access ----------
    _STARTSWITH__ACCESS__OBJECT_LIST: str = "LIST__"

    # -----------------
    _GROUPS: dict[str, Union[Any, list[Any]]] = {}

    # instance ---
    INDEX: int | None = None    # index used only in OBJECT INSTANCE

    def __init__(self, index: int):
        """
        you can use just a simple init (by calling class without index) for generate all instances!
        """
        super().__init__()
        self.INDEX = index
        self.generate__objects()

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def generate__objects(cls) -> None:
        if cls._GROUPS:
            return

        # WORK --------------------------------------
        cls._GROUPS = {}
        for attr_name in dir(cls):
            # LIST --------------------------------------
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_LIST):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_LIST)
                obj_list__name = f"{cls._STARTSWITH__ACCESS__OBJECT_LIST}{group_name}"
                obj_list__value = []
                for index in range(cls.COUNT):
                    # FIXME: add Try sentence
                    obj_cls = getattr(cls, attr_name)
                    obj_instance = obj_cls(index)
                    obj_list__value.append(obj_instance)

                # apply GROUP to class -------
                setattr(cls, obj_list__name, obj_list__value)
                cls._GROUPS.update({group_name: obj_list__value})

            # SINGLE --------------------------------------
            if attr_name.startswith(cls._STARTSWITH__DEFINE__CLS_SINGLE):
                group_name = attr_name.removeprefix(cls._STARTSWITH__DEFINE__CLS_SINGLE)
                # FIXME: add Try sentence
                obj_cls = getattr(cls, attr_name)
                obj_instance = obj_cls()

                # apply -------
                setattr(cls, group_name, obj_instance)
                cls._GROUPS.update({group_name: obj_instance})

    # -----------------------------------------------------------------------------------------------------------------
    def __getattr__(self, item: str) -> Union[None, Any, NoReturn]:
        if self.INDEX is None:
            return

        # ACCESS TO OBJECT ----------------------------
        if self.group_check__exists(item):
            group_objs = self._GROUPS[item]
            if isinstance(group_objs, list):
                obj = group_objs[self.INDEX]
            else:
                obj = group_objs
            return obj

        # FINAL not found -----------------------------
        msg = f"{item=}/{self.INDEX=}"
        print(msg)
        raise Exx__GroupNotExists(msg)

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def group_get__type(cls, name: str) -> GroupType:
        if f"{cls._STARTSWITH__DEFINE__CLS_SINGLE}{name}" in dir(cls):
            return GroupType.SINGLE

        if f"{cls._STARTSWITH__DEFINE__CLS_LIST}{name}" in dir(cls):
            return GroupType.LIST

        return GroupType.NOT_EXISTS

    @classmethod
    def group_check__exists(cls, name: str) -> bool:
        return cls.group_get__type(name) != GroupType.NOT_EXISTS

    @classmethod
    def group_get__objects(cls, name: str) -> Union[None, Any, list[Any]]:
        if cls.group_check__exists(name):
            return cls._GROUPS[name]

    # @classmethod
    # def group_call_meth(cls, meth: str, group: str | None = None) -> Union[NoReturn, TYPE__BREED_RESULT__GROUP, TYPE__BREED_RESULT__GROUPS]:
    #     if group is None:
    #         pass
    #         # call on all groups
    #
    #     if not cls.group_check__exists(group):
    #         raise Exx__BreederGroupNotExists()
    #
    #     else:
    #         :
    #         if
    #         cls._GROUPS[group]:
    #         results = []
    #         for index in range(cls.COUNT):
    #             # FIXME: add Try sentence
    #             obj_instance = getattr(cls, attr_name)(index)
    #             obj_list__value.append(obj_instance)


# =====================================================================================================================
class DevicesIndexed_Base(ObjectListBreeder_Base):
    def __del__(self):
        self.disconnect__cls()

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
    """
    READY TO USE WITH DUT
    """
    # DEFINITIONS ---------------
    CLS_LIST__DUT: Type[DutBase] = DutBase

    # JUST SHOW NAMES -----------
    LIST__DUT: List[DutBase]
    DUT: DutBase


# =====================================================================================================================
class DevicesIndexed_Example(DevicesIndexed_WithDut):
    """
    JUST an example DUT+some other single dev
    """
    # DEFINITIONS ---------------
    COUNT: int = 2
    CLS_SINGLE__ATC: Type[DeviceBase] = DeviceBase

    # JUST SHOW NAMES -----------
    ATC: DeviceBase


# =====================================================================================================================
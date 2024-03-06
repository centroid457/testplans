from typing import *
import uuid

from .tc import TestCaseBase


# =====================================================================================================================
class DeviceBase:
    con: Any = None
    present: Optional[bool] = None

    def mark_present(self) -> None:
        self.present = self.check_present()

    def check_present(self) -> bool:
        return True


# =====================================================================================================================
class DutBase(DeviceBase):
    # SETTINGS ------------------------------------
    SKIP: Optional[bool] = None

    # AUX -----------------------------------
    SN: str = None
    TP_RESULTS: Dict[Type[TestCaseBase], TestCaseBase] = None   # dict is very convenient!!!
    INDEX: int = 0
    DUTS: List[Self] = []

    def __new__(cls, *args, **kwargs):
        instance = super().__new__(cls)
        # instance.INDEX = cls.INDEX
        # cls.INDEX += 1
        instance.INDEX = len(cls.DUTS)
        instance.SN = uuid.uuid4().hex
        cls.DUTS.append(instance)
        return instance

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

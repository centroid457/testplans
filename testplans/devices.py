from typing import *

from .tc import TestCaseBase


# =====================================================================================================================
class DeviceBase:
    present: Optional[bool] = None
    check_present: Callable[..., bool]

    def mark_present(self) -> None:
        self.present = self.check_present()


# =====================================================================================================================
class DutBase(DeviceBase):
    # SETTINGS ------------------------------------
    SKIP: Optional[bool] = None

    # AUXILIARY -----------------------------------
    TP_RESULTS: Dict[Type[TestCaseBase], TestCaseBase] = None   # dict is very convenient!!!

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

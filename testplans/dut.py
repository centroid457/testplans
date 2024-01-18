from typing import *

from .tc import TestCaseBase


# =====================================================================================================================
class DutBase:
    # SETTINGS ------------------------------------
    SKIP: Optional[bool] = None

    # AUXILIARY -----------------------------------
    present: Optional[bool] = None
    check_present: Callable[..., bool]

    TP_RESULTS: Dict[Type[TestCaseBase], TestCaseBase] = None   # dict is very convenient!!!

    def _SKIP_reverse(self) -> None:
        """
        this is only for testing purpose
        """
        self.SKIP = not bool(self.SKIP)

    def mark_present(self) -> None:
        self.present = self.check_present()

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

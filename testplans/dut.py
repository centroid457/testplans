from typing import *

from .tc import TestCase


# =====================================================================================================================
class Dut:
    SKIP: Optional[bool] = None
    PRESENT: Optional[bool] = None
    TP_RESULTS: Dict[Type[TestCase], TestCase] = None   # dict is very convenient!!!

    check_present: Callable[..., bool]

    def mark_present(self) -> None:
        self.PRESENT = self.check_present()

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

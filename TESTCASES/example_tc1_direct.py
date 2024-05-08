import time
from testplans import TestCaseBase

import DEVICES

class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "direct1"

    def run_wrapped(self) -> bool:
        time.sleep(2)
        self.details_update({"detail_value": self.DEVICES__BY_INDEX.DUT.VALUE})
        return self.DEVICES__BY_INDEX.DUT.VALUE

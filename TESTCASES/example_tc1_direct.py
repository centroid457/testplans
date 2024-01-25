import time
from testplans import TestCaseBase

import DEVICES

class TestCase(TestCaseBase):
    ACYNC = False
    DESCRIPTION = "direct1"
    SETTINGS = {}   # DONT DELETE!

    device1: DEVICES.dut_example1.Device    # APPLY any if need!

    def run_wrapped(self) -> bool:
        time.sleep(0.2)
        self.details_update({"detail_value": self.DUT.VALUE})
        return self.DUT.VALUE

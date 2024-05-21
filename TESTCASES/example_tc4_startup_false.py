import time
from testplans import TestCaseBase

import DEVICES

class TestCase123(TestCaseBase):
    ASYNC = False
    DESCRIPTION = "startupCls=False"


    @classmethod
    def startup__cls(cls) -> bool:
        return False

    def run__wrapped(self) -> bool:
        time.sleep(0.2)
        self.details_update({"detail_value": self.DEVICES.DUT.VALUE})
        return self.DEVICES.DUT.VALUE

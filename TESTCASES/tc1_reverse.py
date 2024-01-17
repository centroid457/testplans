import time

from testplans import TestCaseBase
from tc1_direct import TestCase as TC


class TestCase(TC):
    ACYNC = True
    DESCRIPTION = "reverse1"

    def run_wrapped(self) -> bool:
        time.sleep(0.5)
        self.details_update({"detail_value": not self.DUT.VALUE})
        return not self.DUT.VALUE



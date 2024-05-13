import time
from testplans import TestCaseBase
from . import example_tc1_direct


class TestCase(example_tc1_direct.TestCase):
    ASYNC = True
    DESCRIPTION = "reverse1"

    def run__wrapped(self) -> bool:
        time.sleep(0.5)
        self.details_update({"detail_value": not self.DEVICES__BY_INDEX.DUT.VALUE})
        return not self.DEVICES__BY_INDEX.DUT.VALUE

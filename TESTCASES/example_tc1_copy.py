import time
from testplans import TestCaseBase
from . import example_tc1_direct


class TestCase(example_tc1_direct.TestCase):
    DESCRIPTION = "copy1"

    def run_wrapped(self) -> bool:
        self.details_update({"index": self.DUT.INDEX})
        return super().run_wrapped()

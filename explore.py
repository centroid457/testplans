from TESTCASES.example_tc1_direct import TestCase
from testplans import *
from testplans.tp import TestPlanBase

from DEVICES import dev1


# -------------------------------------------
class TestPlan_example1(TestPlanBase):
    TCS = {
        "example_tc1_direct": True,
        "example_tc1_copy": True,
        "example_tc1_reverse": True,
    }

    DUT_CLS = dev1.Device

    SETTINGS_BASE: PrivateJson      # apply for all TCS!!! in settings before create themselves!

    def duts_generate(self) -> None:
        for value in [True, True, False, False, ]:
            self.DUTS.append(self.DUT_CLS(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan_example1()
    TpGui(Tp_obj)


# =====================================================================================================================

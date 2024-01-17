from DEVICES.dev1 import Device
from TESTCASES.tc1_direct import TestCase
from testplans import *
from testplans.tp import TestPlanBase


# -------------------------------------------
class TestPlan1(TestPlanBase):
    TCS = {
        TestCase: True,
        Tc1_reverse: True,
        Tc2: False,
        Tc2_reverse: True,
    }

    def duts_generate(self) -> None:
        for value in [True, True, False, False, ]:
            self.DUTS.append(Device(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan1()
    TpGui(Tp_obj)


# =====================================================================================================================

from testplans import *
from testplans.tp import TpMultyDutBase

from DEVICES import dut_example1


# =====================================================================================================================
class TestPlan_example1(TpMultyDutBase):
    START_GUI = True

    def duts_generate(self) -> None:
        for value in [True, True, False, False, ]:
            self.DUTS.append(dut_example1.Device(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan_example1()


# =====================================================================================================================

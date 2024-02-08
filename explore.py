from testplans import *
from testplans.main import TpMultyDutBase

from DEVICES import dut_example1


# =====================================================================================================================
class TestPlan_example1(TpMultyDutBase):
    def duts_generate(self) -> None:
        for value in [*[True, ] * 5, *[False, ] * 5, ]:
            self.DUTS.append(dut_example1.Device(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan_example1()


# =====================================================================================================================

from testplans import *
from testplans.tp import TpMultyDutBase

from DEVICES import dut_example1


# -------------------------------------------
class TestPlan_example1(TpMultyDutBase):
    DUT_CLS = dut_example1.Device
    SETTINGS_BASE: PrivateJson      # apply for all TCS!!! in settings before create themselves!

    def duts_generate(self) -> None:
        for value in [True, True, False, False, ]:
            self.DUTS.append(self.DUT_CLS(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan_example1()
    TpGui(Tp_obj)


# =====================================================================================================================

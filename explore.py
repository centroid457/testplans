from testplans import *
from testplans.tp import TpManager
from testplans.dut import Dut

import time


# =====================================================================================================================
if __name__ == "__main__":
    class Dut1(Dut):
        def __init__(self, value: Any):
            self.VALUE = value
        def check_present(self) -> bool:
            return True

    # -------------------------------------------
    class Tc1(TestCase):
        PARALLEL = False
        DESCRIPTION = "DESCRIPTION"
        def run_wrapped(self) -> bool:
            time.sleep(0.5)
            self.details_update({"detail_value": self.DUT.VALUE})
            return self.DUT.VALUE

    class Tc1_reverse(TestCase):
        PARALLEL = True
        def run_wrapped(self) -> bool:
            time.sleep(0.5)
            return not self.DUT.VALUE

    class Tc2(Tc1):
        pass

    class Tc2_reverse(Tc1_reverse):
        pass

    # -------------------------------------------
    class TpManager1(TpManager):
        TCS = {
            Tc1: True,
            Tc1_reverse: True,
            Tc2: False,
            Tc2_reverse: True,
        }
        def duts_generate(self) -> None:
            for value in [True, True, False, False, ]:
                self.DUTS.append(Dut1(value))


    Tp_obj = TpManager1()
    TpGui(Tp_obj)


# =====================================================================================================================

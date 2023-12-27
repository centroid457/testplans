from testplan import *
from testplan.tp import Dut, TpManager


# =====================================================================================================================
if __name__ == "__main__":
    class Dut1(Dut):
        def __init__(self, value: Any):
            self.VALUE = value

        def check_present(self) -> bool:
            return True

    # -------------------------------------------
    class Tc1(TestCase):
        def run_wrapped(self) -> bool:
            return self.DUT.VALUE

    class Tc1_reverse(TestCase):
        def run_wrapped(self) -> bool:
            return not self.DUT.VALUE

    class TpManager1(TpManager):
        TCS = {
            Tc1: True,
            Tc1_reverse: False,
        }

        def duts_generate(self) -> None:
            for value in [True, False, ]:
                self.DUTS.append(Dut1(value))


    Tp_obj = TpManager1()
    TpGui(Tp_obj)


# =====================================================================================================================

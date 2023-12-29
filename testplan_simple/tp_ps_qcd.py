from . import TpManager, Dut
from .tc import *

from singleton_meta import *


# duts =================================================================================================================
class DutPs(Dut):
    POSITION: int = None

    def __init__(self, position: int):
        self.POSITION = position

    def check_present(self) -> bool:
        return True

    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!


class _BasePs:
    DUT: DutPs


# TC_STEPS ============================================================================================================
class PsQcd_Tc1(TestCase, _BasePs):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tc2(TestCase, _BasePs):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tc3(TestCase, _BasePs):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tc4(TestCase, _BasePs):
    def run_wrapped(self) -> bool:
        pass


# TC ==================================================================================================================
# class PsQcd_Tc1(TestCase):
#     details = {
#         PsQcd_Tcs1: True,
#         PsQcd_Tcs2: True,
#     }
#
#
# class PsQcd_Tc2(TestCase):
#     details = {
#         PsQcd_Tcs3: True,
#         PsQcd_Tcs4: True,
#     }


# TP ==================================================================================================================
class PsQcd_Tp(TestPlan, _BasePs):
    details = {
        PsQcd_Tc1: True,
        PsQcd_Tc2: True,
        PsQcd_Tc3: True,
        PsQcd_Tc4: False,
    }


# =====================================================================================================================
class ATF(SingletonByCallMeta):
    pass


# =====================================================================================================================
class Manager_PsQcd(TpManager):
    COUNT: int = 10
    ITEMS: Dict[PsQcd_Tp, Any] = {
        # PsQcd_Tp(1): None,
        # PsQcd_Tp(2): None,
    }

    def items_generate(self):
        for port in range(self.COUNT):
            self.ITEMS.update({PsQcd_Tp(DutPs(port)): None})


# =====================================================================================================================

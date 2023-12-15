from .base import *


# DUT =================================================================================================================
class DutPs:
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


class _Base:
    DUT: DutPs


# TC_STEPS ============================================================================================================
class PsQcd_Tc1(TestCase, _Base):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tc2(TestCase, _Base):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tc3(TestCase, _Base):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tc4(TestCase, _Base):
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
class PsQcd_Tp(TestPlan, _Base):
    details = {
        PsQcd_Tc1: True,
        PsQcd_Tc2: True,
        PsQcd_Tc3: True,
        PsQcd_Tc4: False,
    }


# =====================================================================================================================

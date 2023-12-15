from .base import *


# DUT =================================================================================================================
class DutPs:
    POSITION: int = None

    def __init__(self, position: int):
        self.POSITION = position

    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!
    # TODO: FINISH!!!


# TC_STEPS ============================================================================================================
class PsQcd_Tcs1(TestCaseStep):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tcs2(TestCaseStep):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tcs3(TestCaseStep):
    def run_wrapped(self) -> bool:
        pass


class PsQcd_Tcs4(TestCaseStep):
    def run_wrapped(self) -> bool:
        pass


# TC ==================================================================================================================
class PsQcd_Tc1(TestCase):
    details = {
        PsQcd_Tcs1: True,
        PsQcd_Tcs2: True,
    }


class PsQcd_Tc2(TestCase):
    details = {
        PsQcd_Tcs3: True,
        PsQcd_Tcs4: True,
    }


# TP ==================================================================================================================
class PsQcd_Tp(TestPlan):
    details = {
        PsQcd_Tc1: True,
        PsQcd_Tc2: True,
    }


# =====================================================================================================================

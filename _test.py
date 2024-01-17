import time

import pytest

from testplans import *
from testplans.tp import TestPlanBase
from testplans.dut import DutBase


# =====================================================================================================================
class Test__1:
    VICTIM: Type[TestPlanBase] = type("VICTIM", (TestPlanBase,), {})

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (TestPlanBase,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__simple(self):
        # -------------------------------------------
        class M1_Dut(DutBase):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        # -------------------------------------------
        class Tc1(TestCaseBase):
            def run_wrapped(self) -> bool:
                return self.DUT.VALUE

        class Tc1_reverse(TestCaseBase):
            def run_wrapped(self) -> bool:
                return not self.DUT.VALUE

        # -------------------------------------------
        class TestPlan1(TestPlanBase):
            TCS = {
                Tc1: True,
                Tc1_reverse: False
            }
            def duts_generate(self) -> None:
                for value in [True, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = TestPlan1()
        Tp_obj.run()
        assert Tp_obj.DUTS[0].check_result_final() is True

        assert len(Tp_obj.DUTS) == 1

        # -------------------------------------------
        class TestPlan2(TestPlanBase):
            TCS = {
                Tc1: True,
                Tc1_reverse: False
            }
            def duts_generate(self) -> None:
                for value in [False, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = TestPlan2()
        Tp_obj.run()
        assert Tp_obj.DUTS[0].check_result_final() is False

        # -------------------------------------------
        assert len(Tp_obj.DUTS) == 1

    def test__parallel(self):
        # -------------------------------------------
        class M1_Dut(DutBase):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        # -------------------------------------------
        class Tc1(TestCaseBase):
            ACYNC = True
            def run_wrapped(self) -> bool:
                time.sleep(0.5)
                return self.DUT.VALUE

        # -------------------------------------------
        class TestPlan1(TestPlanBase):
            TCS = {
                Tc1: True,
            }
            def duts_generate(self) -> None:
                for value in [True, True, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = TestPlan1()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert 0.5 <= time_passed <= 0.9

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

        # -------------------------------------------
        Tc1.ACYNC = False

        Tp_obj = TestPlan1()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert time_passed >= 1

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

        # -------------------------------------------

    def test__skip(self):
        # -------------------------------------------
        class M1_Dut(DutBase):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        # -------------------------------------------
        class Tc1(TestCaseBase):
            def run_wrapped(self) -> bool:
                time.sleep(0.5)
                return self.DUT.VALUE
        class TestPlan1(TestPlanBase):
            TCS = {
                Tc1: False,
            }
            def duts_generate(self) -> None:
                for value in [False, False, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = TestPlan1()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert time_passed <= 0.2

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

    def test__GUI(self):
        # -------------------------------------------
        class M1_Dut(DutBase):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        # -------------------------------------------
        class Tc1(TestCaseBase):
            def run_wrapped(self) -> bool:
                return self.DUT.VALUE

        class Tc1_reverse(TestCaseBase):
            def run_wrapped(self) -> bool:
                return not self.DUT.VALUE
        class TestPlan1(TestPlanBase):
            TCS = {
                Tc1: True,
                Tc1_reverse: False,
            }
            def duts_generate(self) -> None:
                for value in [False, False, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = TestPlan1()

        with pytest.raises(SystemExit) as exx:
            TpGui(Tp_obj)
        assert exx.type == SystemExit
        assert exx.value.code == 0


# =====================================================================================================================

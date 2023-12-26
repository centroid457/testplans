import time

import pytest

from ps_qcd import *
from ps_qcd.tp import Dut, ManagerTp


# =====================================================================================================================
class Test__1:
    VICTIM: Type[ManagerTp] = type("VICTIM", (ManagerTp,), {})

    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (ManagerTp,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__simple(self):
        # -------------------------------------------
        class M1_Dut(Dut):
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

        # -------------------------------------------
        class Tp1_ManagerTp(ManagerTp):
            TCS = {
                Tc1: True,
                Tc1_reverse: False
            }
            def duts_generate(self) -> None:
                for value in [True, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = Tp1_ManagerTp()
        Tp_obj.run()
        assert Tp_obj.DUTS[0].check_result_final() is True

        assert len(Tp_obj.DUTS) == 1

        # -------------------------------------------
        class Tp2_ManagerTp(ManagerTp):
            TCS = {
                Tc1: True,
                Tc1_reverse: False
            }
            def duts_generate(self) -> None:
                for value in [False, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = Tp2_ManagerTp()
        Tp_obj.run()
        assert Tp_obj.DUTS[0].check_result_final() is False

        # -------------------------------------------
        assert len(Tp_obj.DUTS) == 1

    def test__parallel(self):
        # -------------------------------------------
        class M1_Dut(Dut):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        # -------------------------------------------
        class Tc1(TestCase):
            PARALLEL = True
            def run_wrapped(self) -> bool:
                time.sleep(0.5)
                return self.DUT.VALUE

        # -------------------------------------------
        class Tp1_ManagerTp(ManagerTp):
            TCS = {
                Tc1: True,
            }
            def duts_generate(self) -> None:
                for value in [True, True, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = Tp1_ManagerTp()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert 0.5 <= time_passed <= 0.9

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

        # -------------------------------------------
        Tc1.PARALLEL = False

        Tp_obj = Tp1_ManagerTp()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert time_passed >= 1

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

        # -------------------------------------------

    def test__skip(self):
        # -------------------------------------------
        class M1_Dut(Dut):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        # -------------------------------------------
        class Tc1(TestCase):
            def run_wrapped(self) -> bool:
                time.sleep(0.5)
                return self.DUT.VALUE
        class Tp1_ManagerTp(ManagerTp):
            TCS = {
                Tc1: False,
            }
            def duts_generate(self) -> None:
                for value in [False, False, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = Tp1_ManagerTp()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert time_passed <= 0.2

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

    def test__GUI(self):
        # -------------------------------------------
        class M1_Dut(Dut):
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
        class Tp1_ManagerTp(ManagerTp):
            TCS = {
                Tc1: True,
                Tc1_reverse: False,
            }
            def duts_generate(self) -> None:
                for value in [False, False, ]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = Tp1_ManagerTp()

        with pytest.raises(SystemExit) as exx:
            TpGui(Tp_obj)
        assert exx.type == SystemExit
        assert exx.value.code == 0


# =====================================================================================================================

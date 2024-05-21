import time

import pytest

from testplans import *
from testplans.main import TpMultyDutBase
from testplans.devices import DutBase


# =====================================================================================================================
# -------------------------------------------
class Dut1(DutBase):
    def __init__(self, value: Any):
        self.VALUE = value


# -------------------------------------------
class Tc1(TestCaseBase):
    TIME_SLEEP: float = 0.2
    def run__wrapped(self) -> bool:
        time.sleep(self.TIME_SLEEP)
        return self.DEVICES.DUT.VALUE


class Tc1_reverse(TestCaseBase):
    def run__wrapped(self) -> bool:
        return not super().run__wrapped()


# -------------------------------------------
class Tp1(TpMultyDutBase):
    GUI__START = False
    TCS__CLS = {
        Tc1: True,
        Tc1_reverse: False
    }
    def duts_generate(self) -> None:
        for value in [True, True, ]:
            self.DUTS.append(Dut1(value))


# =====================================================================================================================
@pytest.mark.skip
class Test__1:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        self.VICTIM = type("VICTIM", (TpMultyDutBase,), {})

    # -----------------------------------------------------------------------------------------------------------------
    def test__simple(self):
        # -------------------------------------------
        Tp_obj = Tp1()
        Tp_obj.run()
        assert Tp_obj.DUTS[0].check_result_final() is True
        assert len(Tp_obj.DUTS) == 2

        # -------------------------------------------
        class TestPlan2(TpMultyDutBase):
            GUI__START = False
            TCS__CLS = {
                Tc1: True,
                Tc1_reverse: False
            }
            def duts_generate(self) -> None:
                for value in [False, ]:
                    self.DUTS.append(Dut1(value))

        Tp_obj = TestPlan2()
        Tp_obj.run()
        assert Tp_obj.DUTS[0].check_result_final() is False

        # -------------------------------------------
        assert len(Tp_obj.DUTS) == 1

    def test__acync(self):
        class Tp1(TpMultyDutBase):
            GUI__START = False
            TCS__CLS = {
                Tc1: True,
            }
            def duts_generate(self) -> None:
                for value in [True, True, ]:
                    self.DUTS.append(Dut1(value))

        Tp_obj = Tp1()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert Tc1.TIME_SLEEP - 0.1 <= time_passed <= Tc1.TIME_SLEEP * 2

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

        # -------------------------------------------
        Tc1.ASYNC = False

        Tp_obj = Tp1()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert time_passed >= Tc1.TIME_SLEEP * 2

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

        # -------------------------------------------

    def test__skip(self):
        class Tp1(TpMultyDutBase):
            GUI__START = False
            TCS__CLS = {
                Tc1: False,
            }
            def duts_generate(self) -> None:
                for value in [False, False, ]:
                    self.DUTS.append(Dut1(value))

        Tp_obj = Tp1()
        time_start = time.time()
        Tp_obj.run()
        time_passed = time.time() - time_start
        assert time_passed <= 0.2

        assert Tp_obj.DUTS[0].check_result_final() is True
        assert Tp_obj.DUTS[1].check_result_final() is True

    def test__GUI(self):
        class Tp(Tp1):
            GUI__START = True

        with pytest.raises(SystemExit) as exx:
            Tp()
        assert exx.type == SystemExit
        assert exx.value.code == 0

    def test__info_get(self):
        Tp_obj = Tp1()
        info_data = Tp_obj.get__info()
        assert isinstance(info_data, dict)
        assert len(info_data) > 2

    @pytest.mark.skip
    def test__SETTINGS(self):
        pass


# =====================================================================================================================

import os
import pytest
import pathlib
import shutil
from tempfile import TemporaryDirectory
from typing import *
from configparser import ConfigParser

from ps_qcd import *


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
        class M1_Dut(DutWithTp):
            def __init__(self, value: Any):
                self.VALUE = value

            def check_present(self) -> bool:
                return True

        class Tc1(TestCase):
            def run_wrapped(self) -> bool:
                return self.DUT.VALUE

        class Tc2(TestCase):
            def run_wrapped(self) -> bool:
                return self.DUT.VALUE

        class Tp1_ManagerTp(ManagerTp):
            TCS = {
                Tc1: True,
                Tc2: False
            }

            def duts_generate(self) -> None:
                for value in [True, True]:
                    self.DUTS.append(M1_Dut(value))

        Tp_obj = Tp1_ManagerTp()
        Tp_obj.run()
        for dut in Tp_obj.DUTS:
            assert dut.check_result_final() is True


# =====================================================================================================================

import os
import time

import pytest
import pathlib
from typing import *

from testplans import *
from bus_user import *

from DEVICES import atc, ptb


# =====================================================================================================================
# @pytest.mark.skip
class Test__DevicesBreeder_OnSerial:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(DevicesBreeder):
            COUNT = 10
            CLS_SINGLE__ATC = atc.Device
            CLS_LIST__PTB = ptb.Device

        cls.Victim = Victim

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        # 1 -----------------------------------------------------
        assert False


# =====================================================================================================================

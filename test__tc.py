import os
import time

import pytest
import pathlib
import shutil
from typing import *

from testplans import *


# =====================================================================================================================
class DevicesBreeder_Example(DevicesBreeder_WithDut):
    """
    JUST an example DUT+some other single dev
    """
    # DEFINITIONS ---------------
    COUNT: int = 2
    CLS_SINGLE__ATC: Type[DeviceBase] = DeviceBase

    # JUST SHOW NAMES -----------
    ATC: DeviceBase

# =====================================================================================================================
class Test__TestCaseBase:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = TestCaseBase

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     passtest__tc.py
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__cls(self):
        # EXISTS IN CLS --------------
        assert self.Victim.TCS__LIST == []
        assert self.Victim.DEVICES__BREEDER_CLS is None

        assert self.Victim.result__cls_startup is None
        assert self.Victim.result__cls_teardown is None

        # EXISTS IN INSTANCE --------------
        assert not hasattr(self.Victim, "INDEX")
        assert not hasattr(self.Victim, "SETTINGS")
        assert not hasattr(self.Victim, "DEVICES__BREEDER_INST")

        assert not hasattr(self.Victim, "timestamp_start")
        assert not hasattr(self.Victim, "details")
        assert not hasattr(self.Victim, "exx")
        assert not hasattr(self.Victim, "progress")

    def test__devices(self):
        self.Victim.devices__apply()
        assert self.Victim.TCS__LIST == []

        self.Victim.DEVICES__BREEDER_CLS = DevicesBreeder_Example
        self.Victim.devices__apply()
        assert self.Victim.TCS__LIST != []


        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!


# =====================================================================================================================

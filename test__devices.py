import os
import time

import pytest
import pathlib
import shutil
from typing import *

from testplans import *


# =====================================================================================================================
class Test__DeviceBase:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (DeviceBase,), {})

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        victim = self.Victim()
        assert victim.PRESENT is None
        assert victim.check_present() is True
        assert victim.PRESENT is None
        victim._mark_present()
        assert victim.PRESENT is True


# =====================================================================================================================
class Test__DutBase:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (DutBase,), {})

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__1(self):
        victim = self.Victim()
        assert victim.PRESENT is None
        assert victim.check_present() is True
        assert victim.PRESENT is None
        victim._mark_present()
        assert victim.PRESENT is True

    def test__2(self):
        victim = self.Victim()
        assert victim.INDEX is None

        victim = self.Victim(2)
        assert victim.INDEX == 2

        assert victim.check_present() is True
        assert victim.PRESENT is None
        victim._mark_present()
        assert victim.PRESENT is True


# =====================================================================================================================
class Test__TpDevicesIndexed:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim: Type[TpDevicesIndexed] = type("Victim", (TpDevicesIndexed,), {})

    # @classmethod
    # def teardown_class(cls):
    #     pass
    #
    # def setup_method(self, method):
    #     pass
    #
    # def teardown_method(self, method):
    #     pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__DUT(self):
        # 1 -----------------------------------------------------
        self.Victim.COUNT = 1
        assert self.Victim._GROUPS == {}
        self.Victim.generate__cls()
        assert list(self.Victim._GROUPS) == ["DUT", ]
        assert len(self.Victim._GROUPS["DUT"]) == 1
        assert self.Victim._GROUPS["DUT"] == self.Victim.LIST__DUT
        assert type(self.Victim._GROUPS["DUT"][0]) == DutBase

        victim = self.Victim(0)
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]

        # 2 ------------------------------------------------------
        self.Victim.COUNT = 2
        self.Victim._GROUPS = {}
        self.Victim.generate__cls()
        assert list(self.Victim._GROUPS) == ["DUT", ]
        assert len(self.Victim._GROUPS["DUT"]) == 2
        assert self.Victim._GROUPS["DUT"] == self.Victim.LIST__DUT
        assert type(self.Victim._GROUPS["DUT"][0]) == DutBase

        victim = self.Victim(0)
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]

        victim = self.Victim(1)
        assert victim.DUT == self.Victim.LIST__DUT[1]
        assert victim.DUT == victim.LIST__DUT[1]

        assert victim.LIST__DUT[0] != victim.LIST__DUT[1]
        assert self.Victim.LIST__DUT[0] != self.Victim.LIST__DUT[1]

    def test__CLS_SINGLE(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_SINGLE__ATC = DeviceBase
        self.Victim.generate__cls()

        assert list(self.Victim._GROUPS) == ["DUT", ]
        assert len(self.Victim._GROUPS["DUT"]) == 2
        assert self.Victim._GROUPS["DUT"] == self.Victim.LIST__DUT
        assert type(self.Victim._GROUPS["DUT"][0]) == DutBase

        victim = self.Victim(0)
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]


# =====================================================================================================================

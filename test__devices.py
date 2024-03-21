import os
import time

import pytest
import pathlib
import shutil
from typing import *

from testplans import *
from bus_user import *


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

    def test__2(self):
        victim = self.Victim()
        assert victim.INDEX is None

        victim = self.Victim(2)
        assert victim.INDEX == 2


# =====================================================================================================================
class Test__TpDevicesIndexed:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass

    def setup_method(self, method):
        pass
        self.Victim: Type[DevicesIndexed_WithDut] = type("Victim", (DevicesIndexed_WithDut,), {})

    def teardown_method(self, method):
        pass

    # -----------------------------------------------------------------------------------------------------------------
    def test__DUT_COUNT(self):
        # 1 -----------------------------------------------------
        self.Victim.COUNT = 1
        assert self.Victim._GROUPS == {}
        self.Victim.init__devices()

        assert set(self.Victim._GROUPS) == {"DUT", }
        assert len(self.Victim._GROUPS["DUT"]) == 1
        assert self.Victim._GROUPS["DUT"] == self.Victim.LIST__DUT
        assert type(self.Victim._GROUPS["DUT"][0]) == DutBase

        victim = self.Victim(0)
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]

        # 2 ------------------------------------------------------
        self.Victim.COUNT = 2
        self.Victim._GROUPS = {}
        self.Victim.init__devices()

        assert set(self.Victim._GROUPS) == {"DUT", }
        assert len(self.Victim._GROUPS["DUT"]) == 2
        assert self.Victim._GROUPS["DUT"] == self.Victim.LIST__DUT
        assert type(self.Victim._GROUPS["DUT"][0]) == DutBase

        # INSTANCE ----------------------
        victim = self.Victim(0)
        assert victim.DUT == self.Victim.LIST__DUT[0]
        assert victim.DUT == victim.LIST__DUT[0]

        victim = self.Victim(1)
        assert victim.DUT == self.Victim.LIST__DUT[1]
        assert victim.DUT == victim.LIST__DUT[1]

        assert victim.LIST__DUT[0] != victim.LIST__DUT[1]
        assert self.Victim.LIST__DUT[0] != self.Victim.LIST__DUT[1]

    # -----------------------------------------------------------------------------------------------------------------
    def test__CLS_SINGLE__CLS(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_SINGLE__ATC = DeviceBase
        self.Victim.init__devices()

        assert set(self.Victim._GROUPS) == {"DUT", "ATC"}

        assert type(self.Victim._GROUPS["DUT"]) == list
        assert type(self.Victim._GROUPS["ATC"]) == DeviceBase

        atc_old = self.Victim._GROUPS["ATC"]

        assert hasattr(self.Victim, "LIST__DUT") is True
        assert hasattr(self.Victim, "LIST__ATC") is False

        assert self.Victim.LIST__DUT == self.Victim._GROUPS["DUT"]
        assert self.Victim.ATC == self.Victim._GROUPS["ATC"]

        assert self.Victim.check_exists__group__("DUT") is True
        assert self.Victim.check_exists__group__("ATC") is True
        assert self.Victim.check_exists__group__("PTS") is False

        # DISCONNECT
        self.Victim.disconnect__cls()
        assert id(atc_old) == id(self.Victim.ATC)
        assert atc_old is self.Victim.ATC

        self.Victim.init__devices()
        assert id(atc_old) == id(self.Victim.ATC)
        assert atc_old is self.Victim.ATC

    def test__CLS_SINGLE__INSTANCE(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_SINGLE__ATC = DeviceBase

        victim = self.Victim(1)

        assert set(victim._GROUPS) == {"DUT", "ATC"}

        assert type(victim._GROUPS["DUT"]) == list
        assert type(victim._GROUPS["ATC"]) == DeviceBase

        assert victim.DUT == victim.LIST__DUT[1]
        assert victim.ATC == victim._GROUPS["ATC"]
        try:
            victim.PTS
            assert False
        except:
            pass

        assert hasattr(victim, "LIST__DUT") is True
        try:
            hasattr(victim, "LIST__ATC")
            assert False
        except:
            pass

        assert victim.LIST__DUT == victim._GROUPS["DUT"]

        assert victim.check_exists__group__("DUT") is True
        assert victim.check_exists__group__("ATC") is True
        assert victim.check_exists__group__("PTS") is False

    # -----------------------------------------------------------------------------------------------------------------
    def test__CLS_LIST__CLS(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_LIST__PTS = DeviceBase
        self.Victim.init__devices()

        assert set(self.Victim._GROUPS) == {"DUT", "PTS"}

        assert type(self.Victim._GROUPS["DUT"]) == list
        assert type(self.Victim._GROUPS["PTS"]) == list

        assert hasattr(self.Victim, "LIST__DUT") is True
        assert hasattr(self.Victim, "LIST__PTS") is True

        assert self.Victim.LIST__DUT == self.Victim._GROUPS["DUT"]
        assert self.Victim.LIST__PTS == self.Victim._GROUPS["PTS"]

        assert len(self.Victim.LIST__DUT) == 2
        assert len(self.Victim.LIST__PTS) == 2

        assert self.Victim.check_exists__group__("DUT") is True
        assert self.Victim.check_exists__group__("ATC") is False
        assert self.Victim.check_exists__group__("PTS") is True

    def test__CLS_LIST__INSTANCE(self):
        self.Victim.COUNT = 2
        self.Victim.CLS_LIST__PTS = DeviceBase

        victim = self.Victim(1)

        assert set(victim._GROUPS) == {"DUT", "PTS"}

        assert type(victim._GROUPS["DUT"]) == list
        assert type(victim._GROUPS["PTS"]) == list

        assert victim.DUT == victim.LIST__DUT[1]
        assert victim.PTS == victim.LIST__PTS[1]
        try:
            victim.ATC
            assert False
        except:
            pass

        assert hasattr(victim, "LIST__DUT") is True
        assert hasattr(victim, "LIST__PTS") is True

        assert victim.LIST__DUT == victim._GROUPS["DUT"]
        assert victim.LIST__PTS == victim._GROUPS["PTS"]

        assert len(victim.LIST__DUT) == 2
        assert len(victim.LIST__PTS) == 2

        assert victim.check_exists__group__("DUT") is True
        assert victim.check_exists__group__("ATC") is False
        assert victim.check_exists__group__("PTS") is True

    # -----------------------------------------------------------------------------------------------------------------
    def test__double_init(self):
        # insts is the same!
        pass

    # def reconnect


# =====================================================================================================================

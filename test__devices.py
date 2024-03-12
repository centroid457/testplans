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
        victim.mark_present()
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
        victim.mark_present()
        assert victim.PRESENT is True

    def test__2(self):
        victim = self.Victim()
        assert victim.INDEX is None

        victim = self.Victim(2)
        assert victim.INDEX == 2

        assert victim.check_present() is True
        assert victim.PRESENT is None
        victim.mark_present()
        assert victim.PRESENT is True


# =====================================================================================================================

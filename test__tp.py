import os
import time

import pytest
import pathlib
import shutil
from typing import *

from testplans import *
from bus_user import *


# =====================================================================================================================
class Test__Tp:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(TpMultyDutBase):
            pass

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
    def test__1(self):
        victim = self.Victim()
        assert not victim.DEVICES__CLS
        assert not victim.DEVICES__BY_INDEX
        assert not victim.INDEX
        assert not victim.TCS__INST
        assert victim.ready == TcReadyState.NOT_CHECKED

        assert not victim.result
        assert not victim.details
        assert not victim.exx
        assert victim.progress == 0

        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!
        # TODO: FINISH!


# =====================================================================================================================

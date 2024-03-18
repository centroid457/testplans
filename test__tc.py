import os
import time

import pytest
import pathlib
import shutil
from typing import *

from testplans import *


# =====================================================================================================================
class Test__TestCaseBase:
    @classmethod
    def setup_class(cls):
        pass
        cls.Victim = type("Victim", (TestCaseBase,), {})

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
        assert not victim.DEVICES__CLS
        assert not victim.DEVICES__BY_INDEX
        assert not victim.INDEX
        assert not victim.TCS__INST
        assert victim.ready == TcReadyState.NOT_CHECKED

        assert not victim.result
        assert not victim.details
        assert not victim.exx
        assert victim.progress == 0





# =====================================================================================================================

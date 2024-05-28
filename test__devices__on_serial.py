import os
import time

import pytest
import pathlib
from typing import *

from testplans import *
from bus_user import *


# =====================================================================================================================
class _Atc_SerialClient(SerialClient):
    ADDRESS = Type__AddressAutoAcceptVariant.FIRST_FREE__PAIRED
    RAISE_CONNECT = False

    # EMULATOR ------------------------
    # _EMULATOR__CLS = SerialServer_Example
    # _EMULATOR__START = True


class Atc(DeviceBase):
    conn = _Atc_SerialClient()

    # OVERWRITE =======================================================================================================
    pass
    pass
    pass
    pass


# =====================================================================================================================
@pytest.mark.skip
class Test__TpDevicesIndexed_OnSerial:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(DevicesBreeder_Example):
            COUNT = 2
            CLS_SINGLE__ATC = Atc

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

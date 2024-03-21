import os
import time

import pytest
import pathlib
from typing import *

from testplans import *
from bus_user import *


# =====================================================================================================================
class _Atc_SerialClient(SerialClient):
    ADDRESS = AddressAutoAcceptVariant.FIRST_FREE__PAIRED_FOR_EMU
    RAISE_CONNECT = False

    # EMULATOR ------------------------
    _EMULATOR__CLS = SerialServer_Example
    _EMULATOR__START = True

    def connect__validation(self) -> bool:
        return self.address__answer_validation()

    def address__answer_validation(self) -> bool:
        return self.write_read_line_last("upper hello") == "UPPER HELLO"


class Atc(DeviceBase):
    conn = _Atc_SerialClient()

    # OVERWRITE =======================================================================================================
    pass
    pass
    pass
    pass

    # CONNECT ---------------------------------
    def connect(self) -> bool:
        return self.con.connect()

    def disconnect(self) -> None:
        try:
            self.con.disconnect()
        except:
            pass

    # PRESENT -----------------------------------
    def selftest(self) -> Optional[bool]:
        """
        :return: None - not implemented (lets decide it!)
        """
        pass


# =====================================================================================================================
# @pytest.mark.skip
class Test__TpDevicesIndexed_OnSerial:
    @classmethod
    def setup_class(cls):
        pass

        class Victim(DevicesIndexed_Example):
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
        assert self.Victim._GROUPS == {}
        self.Victim.generate__devices()
        assert self.Victim._GROUPS != {}


# =====================================================================================================================

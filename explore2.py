# DON'T DELETE!
# useful to start smth without pytest and not to run in main script!

from typing import *
from server_templates import ServerAiohttpBase, Client_RequestsStack, Client_RequestItem
from testplans import *

from DEVICES import dut_example1
from bus_user import *


# =====================================================================================================================
class Atc_SerialClient(SerialClient):
    RAISE_CONNECT = False

    # ADDRESS = AddressAutoAcceptVariant.FIRST_FREE__PAIRED_FOR_EMU
    ADDRESS = Type__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID
    # ADDRESS = "COM24"
    # ADDRESS = "/dev/ttyUSB0"
    BAUDRATE = 115200
    PREFIX = "ATC:03:"
    EOL__SEND = b"\r"

    # EMULATOR ------------------------
    # _EMULATOR__CLS = Atc_Emulator
    # _EMULATOR__START = True

    def address__answer_validation(self) -> bool:
        return self.write_read_line_last("get name") == "ATC 03"

class Atc(DeviceBase):
    conn = Atc_SerialClient()


# ---------------------------------------------------------------------------------------------------------------------
class Ptb_SerialClient(SerialClient):
    # ADDRESS = AddressAutoAcceptVariant.FIRST_FREE__PAIRED_FOR_EMU
    ADDRESS = Type__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID
    RAISE_CONNECT = False

    INDEX: int | None

    # EMULATOR ------------------------
    # _EMULATOR__CLS = Ptb_Emulator
    # _EMULATOR__START = True

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX}:"

    def address__answer_validation(self) -> bool:
        return self.write_read_line_last("get name") == f"PTB {self.INDEX}"


class Ptb(DeviceBase):
    conn = Ptb_SerialClient()


# ---------------------------------------------------------------------------------------------------------------------
class Dut(DutBase):
    __sn_start: str = "SN"

    BREEDER: 'DevicesBreeder'

    def connect(self):
        return self.BREEDER.PTB.connect()

    @property
    def VALUE(self) -> bool:
        return self.INDEX % 2 == 0

    @property
    def SN(self) -> str:
        return f"{self.__sn_start}_{self.INDEX}"

    @SN.setter
    def SN(self, value: Any) -> None:
        self.__sn_start = str(value).upper()


# ---------------------------------------------------------------------------------------------------------------------
class DevicesBreeder__Tp(DevicesBreeder_WithDut):
    COUNT = 3
    CLS_SINGLE__ATC = Atc
    CLS_LIST__PTB = Ptb
    CLS_LIST__DUT = Dut


# =====================================================================================================================
class Client_RequestItem_Tp(Client_RequestItem):
    LOG_ENABLE = True

    RETRY_LIMIT = 0
    RETRY_TIMEOUT = 1

    HOST: str = "192.168.74.20"
    PORT: int = 8080
    ROUTE: str = "results"

    SUCCESS_IF_FAIL_CODE = True


class Client_RequestsStack_Tp(Client_RequestsStack):
    LOG_ENABLE = True
    REQUEST_CLS = Client_RequestItem_Tp


# =====================================================================================================================
class Tp_Example(TpMultyDutBase):
    LOG_ENABLE = True
    api_client: Client_RequestsStack = Client_RequestsStack_Tp()
    # api_client: Client_RequestsStack = None

    DEVICES__BREEDER_CLS = DevicesBreeder__Tp

    API_SERVER__CLS = TpApi_FastApi

    GUI__START = True
    API_SERVER__START = True


# =====================================================================================================================
class TpInsideApi_Runner__example(TpInsideApi_Runner):
    TP_CLS = Tp_Example


# =====================================================================================================================
def run_direct():
    Tp_Example()


def run_over_api():
    TpInsideApi_Runner__example()


# =====================================================================================================================
if __name__ == "__main__":
    run_direct()
    # run_over_api()


# =====================================================================================================================

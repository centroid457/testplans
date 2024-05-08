from testplans import *
from testplans.main import TpMultyDutBase, DevicesIndexed_WithDut, TpInsideApi_Runner
from server_templates import ServerAiohttpBase, Client_RequestsStack, Client_RequestItem

from DEVICES import dut_example1


# =====================================================================================================================
class DevicesIndexed__Tp(DevicesIndexed_WithDut):
    COUNT = 3
    CLS_LIST__DUT = dut_example1.Device


# =====================================================================================================================
class Client_RequestItem_Tp(Client_RequestItem):
    pass
    HOST: str = "192.168.74.20"
    PORT: int = 8080
    ROUTE: str = "results"


class Client_RequestsStack_Tp(Client_RequestsStack):
    REQUEST_CLS = Client_RequestItem_Tp


# =====================================================================================================================
class Tp_Example(TpMultyDutBase):
    # api_client: Client_RequestsStack = Client_RequestsStack_Tp()
    api_client: Client_RequestsStack = None

    DEVICES__CLS = DevicesIndexed__Tp

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

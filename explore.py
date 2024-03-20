from testplans import *
from testplans.main import TpMultyDutBase, DevicesIndexed_WithDut
from server_templates import ServerAiohttpBase, Client_RequestsStack, Client_RequestItem

from DEVICES import dut_example1


# =====================================================================================================================
class DevicesIndexed__Example(DevicesIndexed_WithDut):
    COUNT = 4
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
    api_client: Client_RequestsStack = Client_RequestsStack_Tp()
    DEVICES__CLS = DevicesIndexed__Example


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = Tp_Example()


# =====================================================================================================================

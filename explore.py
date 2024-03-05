from testplans import *
from testplans.main import TpMultyDutBase
from server_templates import ServerAiohttpBase, Client_RequestsStack, Client_RequestItem

from DEVICES import dut_example1


# =====================================================================================================================
class Client_RequestItem_Tp(Client_RequestItem):
    pass
    HOST: str = "192.168.74.20"
    PORT: int = 8080
    ROUTE: str = "results"


class Client_RequestsStack_Tp(Client_RequestsStack):
    REQUEST_CLS = Client_RequestItem_Tp


# =====================================================================================================================
class TestPlan_example1(TpMultyDutBase):
    api_client: Client_RequestsStack = Client_RequestsStack_Tp()

    def duts_generate(self) -> None:
        for value in [*[True, ] * 1, *[False, ] * 1, ]:
            self.DUTS.append(dut_example1.Device(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan_example1()


# =====================================================================================================================

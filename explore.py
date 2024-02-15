from testplans import *
from testplans.main import TpMultyDutBase
from server_templates import ServerAiohttpBase, RequestsStack, RequestItem

from DEVICES import dut_example1


# =====================================================================================================================
class RequestItem_Tp(RequestItem):
    pass
    HOST: str = "192.168.74.20"
    PORT: int = 8080
    ROUTE: str = "results"


class RequestsStack_Tp(RequestsStack):
    REQUEST_CLS = RequestItem_Tp


# =====================================================================================================================
class TestPlan_example1(TpMultyDutBase):
    api_client: RequestsStack = RequestsStack_Tp()

    def duts_generate(self) -> None:
        for value in [*[True, ] * 1, *[False, ] * 1, ]:
            self.DUTS.append(dut_example1.Device(value))


# =====================================================================================================================
if __name__ == "__main__":
    Tp_obj = TestPlan_example1()


# =====================================================================================================================

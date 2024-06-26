import time
from testplans import *
from funcs_aux import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "ptb"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True
        # result_chain = ResultExpect_Chain(
        #     [
        #         ResultExpect_Step(value=hasattr(cls, "DEVICES__BREEDER_CLS"), value_under_func=bool, title="hasattr DEVICES__CLS"),
        #         ResultExpect_Step(value=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), value_under_func=bool, title="hasattr ATC"),
        #         ResultExpect_Step(value=cls.DEVICES__BREEDER_CLS.ATC.connect, title="ATC.connect()"),
        #     ],
        # )
        # return result_chain

    def startup__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        result = ResultExpect_Chain(
            [
                ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.connect__only_if_address_resolved, title="DUT.connect__only_if_address_resolved"),
            ],
        )
        return result

    def run__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        # time.sleep(0.1)
        result = ResultExpect_Chain(
            [
                ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.connect__only_if_address_resolved, title="DUT.connect__only_if_address_resolved"),
            ],
        )
        return result


# =====================================================================================================================

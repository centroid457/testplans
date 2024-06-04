import time
from testplans import TestCaseBase, TYPE__RESULT

from funcs_aux import ResultExpect_Step, ResultExpect_Chain


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = False
    DESCRIPTION = "serial"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT:
        return True
        # result_chain = ResultExpect_Chain(
        #     [
        #         ResultExpect_Step(value=hasattr(cls, "DEVICES__BREEDER_CLS"), value_under_func=bool, title="hasattr DEVICES__CLS"),
        #         ResultExpect_Step(value=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), value_under_func=bool, title="hasattr ATC"),
        #         ResultExpect_Step(value=cls.DEVICES__BREEDER_CLS.ATC.connect, title="ATC.connect()"),
        #     ],
        # )
        # result_chain.run()
        # return result_chain

    def startup__wrapped(self) -> TYPE__RESULT:
        result_chain = ResultExpect_Chain(
            [
                ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.connect, title="DUT.connect"),
            ],
        )
        result_chain.run()
        return result_chain

    def run__wrapped(self) -> TYPE__RESULT:
        result_chain = ResultExpect_Chain(
            [
                ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.connect, title="DUT.connect"),
            ],
        )
        result_chain.run()
        return result_chain


# =====================================================================================================================

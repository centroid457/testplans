import time
from testplans import TestCaseBase, TYPE__RESULT

from funcs_aux import ResultExpect_Step, ResultExpect_Chain


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "atc"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT:
        result_chain = ResultExpect_Chain(
            [
                ResultExpect_Step(value=hasattr(cls, "DEVICES__BREEDER_CLS"), value_under_func=bool, title="hasattr DEVICES__CLS"),
                ResultExpect_Step(value=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), value_under_func=bool, title="hasattr ATC"),
                ResultExpect_Step(value=cls.DEVICES__BREEDER_CLS.ATC.connect, title="ATC.connect()"),
            ],
        )
        result_chain.run()
        return result_chain

    def run__wrapped(self) -> TYPE__RESULT:
        result_chain = ResultExpect_Chain(
            [
                # ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.VALUE, title="DUT.VALUE"),
                ResultExpect_Step(value=self.DEVICES__BREEDER_INST.ATC.address__answer_validation, title="atc.address__answer_validation"),
            ],
        )
        result_chain.run()
        return result_chain


# =====================================================================================================================
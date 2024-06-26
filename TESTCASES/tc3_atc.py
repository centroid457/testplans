import time
from testplans import *
from funcs_aux import *

from .tc0_groups import *

# =====================================================================================================================
class TestCase(ClsMiddleGroup_ATC220220, TestCaseBase):
    ASYNC = True
    DESCRIPTION = "atc"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        result_chain = ResultExpect_Chain(
            [
                ResultExpect_Step(value=hasattr(cls, "DEVICES__BREEDER_CLS"), value_under_func=bool, title="hasattr DEVICES__CLS"),
                ResultExpect_Step(value=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), value_under_func=bool, title="hasattr ATC"),
                ResultExpect_Step(value=cls.DEVICES__BREEDER_CLS.ATC.connect, title="ATC.connect()"),
            ],
        )
        return result_chain

    def run__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return True
        time.sleep(0.1)
        result_chain = ResultExpect_Chain(
            [
                # ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.VALUE, title="DUT.VALUE"),
                # ResultExpect_Step(value=self.DEVICES__BREEDER_INST.ATC.address__answer_validation, title="atc.address__answer_validation"),
            ],
        )
        return result_chain


# =====================================================================================================================

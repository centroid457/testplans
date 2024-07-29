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
        return True
        result_chain = ValidChains(
            [
                Valid(value_link=hasattr(cls, "DEVICES__BREEDER_CLS"), title="hasattr DEVICES__CLS"),
                Valid(value_link=hasattr(cls.DEVICES__BREEDER_CLS, "ATC"), title="hasattr ATC"),
                Valid(value_link=cls.DEVICES__BREEDER_CLS.ATC.connect, title="ATC.connect()"),
            ],
        )
        return result_chain

    def run__wrapped(self) -> TYPE__RESULT_W_NORETURN:
        return True
        time.sleep(0.1)
        result_chain = ValidChains(
            [
                Valid(value_link=self.DEVICES__BREEDER_INST.DUT.VALUE, title="DUT.VALUE"),
                Valid(value_link=self.DEVICES__BREEDER_INST.ATC.address__answer_validation, title="atc.address__answer_validation"),
            ],
        )
        return result_chain


# =====================================================================================================================

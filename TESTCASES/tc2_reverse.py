import time
from testplans import TestCaseBase, TYPE__RESULT
from . import tc1_direct

from funcs_aux import ResultExpect_Step, ResultExpect_Chain


# =====================================================================================================================
class TestCase(tc1_direct.TestCase):
    ASYNC = True
    DESCRIPTION = "reverse1"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT:
        result_chain = ResultExpect_Chain(
            [
                ResultExpect_Step(value=True, title="TRUE"),
                ResultExpect_Step(value=False, title="FALSE"),
                ResultExpect_Step(value=None, title="NONE"),
            ],
        )
        result_chain.run()
        return result_chain

    def run__wrapped(self) -> bool:
        time.sleep(0.2)
        self.details_update({"detail_value": not self.DEVICES__BREEDER_INST.DUT.VALUE})
        return not self.DEVICES__BREEDER_INST.DUT.VALUE


# =====================================================================================================================

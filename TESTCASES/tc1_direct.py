import time
from testplans import TestCaseBase

from funcs_aux import ResultExpect_Step, ResultExpect_Chain


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "direct1"

    def run__wrapped(self):
        time.sleep(0.2)
        self.details_update({"detail_value": self.DEVICES__BREEDER_INST.DUT.VALUE})

        result_chain = ResultExpect_Chain(
            [
                ResultExpect_Step(value=True, title="TRUE"),
                # ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.VALUE, title="DUT.VALUE"),
            ],
        )

        result_chain.run()
        return result_chain


# =====================================================================================================================

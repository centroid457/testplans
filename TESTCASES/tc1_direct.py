import time
from testplans import *
from funcs_aux import *
from pytest_aux import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "direct1"

    def run__wrapped(self):
        time.sleep(0.1)
        self.details_update({"detail_value": self.DEVICES__BREEDER_INST.DUT.VALUE})
        # result_chain = ResultExpect_Chain(
        #     [
        #         ResultExpect_Step(value=True, title="TRUE"),
        #         # ResultExpect_Step(value=self.DEVICES__BREEDER_INST.DUT.VALUE, title="DUT.VALUE"),
        #     ],
        # )

        result = ResultCum()
        result.result__apply_step(True)
        result.result__apply_step(True, msg="TRUE")
        result.result__apply_step(False, False, msg="FALSE")
        result.result__apply_step(ValueValidate(True))
        result.result__apply_step(ValueValidate(LAMBDA_TRUE), msg="extraLine")
        return result


# =====================================================================================================================

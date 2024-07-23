import time
from testplans import *
from funcs_aux import *
from pytest_aux import *

from . import tc1_direct
from .tc0_groups import *


# =====================================================================================================================
class TestCase(ClsMiddleGroup_ATC220220, tc1_direct.TestCase):
    ASYNC = True
    DESCRIPTION = "reverse1"

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        # result_chain = ResultExpect_Chain(
        #     [
        #         ResultExpect_Step(value=True, title="TRUE"),
        #         ResultExpect_Step(value=False, title="FALSE"),
        #         ResultExpect_Step(value=None, title="NONE"),
        #     ],
        # )

        result = ResultCum()
        result.result__apply_step(True)
        result.result__apply_step(True, msg="TRUE")
        result.result__apply_step(False, False, msg="FALSE")
        result.result__apply_step(ValueValidate(True))
        result.result__apply_step(ValueValidate(LAMBDA_TRUE), msg="extraLine")
        return result

    def run__wrapped(self) -> bool:
        time.sleep(0.1)
        self.details_update({"detail_value": not self.DEVICES__BREEDER_INST.DUT.VALUE})
        return not self.DEVICES__BREEDER_INST.DUT.VALUE


# =====================================================================================================================

from typing import *
from testplans import TestCaseBase, TYPE__RESULT_W_EXX
from funcs_aux import *


# =====================================================================================================================
class TestCase(TestCaseBase):
    ASYNC = True
    DESCRIPTION = "PTB exist"

    # RUN -------------------------------------------------------------------------------------------------------------
    def run__wrapped(self) -> TYPE__RESULT_W_EXX:
        result = Valid(
            value_link=self.DEVICES__BREEDER_INST.DUT.connect__only_if_address_resolved,
            name="DUT.connect__only_if_address_resolved"
        )
        return result


# =====================================================================================================================

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
        result_chain = ValidChains(
            [
                Valid(value_link=True, name="TRUE"),
                Valid(value_link=False, name="FALSE"),
                Valid(value_link=None, name="NONE"),
            ],
        )
        return result_chain

    def run__wrapped(self) -> bool:
        time.sleep(0.1)
        self.details_update({"detail_value": not self.DEVICES__BREEDER_INST.DUT.VALUE})
        return not self.DEVICES__BREEDER_INST.DUT.VALUE


# =====================================================================================================================

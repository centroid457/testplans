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
        result_chain = ValidChains(
            [
                Valid(value_link=True, name="TRUE"),
                Valid(value_link=self.DEVICES__BREEDER_INST.DUT.VALUE, name="DUT.VALUE"),
                Valid(
                    value_link=lambda: self.DEVICES__BREEDER_INST.DUT.connect__only_if_address_resolved(),
                    name="DUT.connect__only_if_address_resolved"
                ),
            ],
        )
        return result_chain


# =====================================================================================================================

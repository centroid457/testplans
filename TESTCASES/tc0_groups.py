from testplans import *
from testplans import TYPE__RESULT_W_NORETURN
from funcs_aux import *


# =====================================================================================================================
class TcGroup_ATC220220(TcGroup_Base):
    MIDDLE_GROUP__NAME = "ATC230220"

    # HERE ARE PLACE CLSMETHs
    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

# =====================================================================================================================

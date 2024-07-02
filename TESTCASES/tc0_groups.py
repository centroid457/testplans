import time
from testplans import *
from funcs_aux import *
from classes_aux import *


# =====================================================================================================================
class ClsMiddleGroup_ATC220220(ClsMiddleGroup_TpBase):
    @classmethod
    def startup__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True


# =====================================================================================================================

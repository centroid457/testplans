from testplans import *
from testplans import TYPE__RESULT_W_NORETURN


# =====================================================================================================================
class ClsMiddleGroup_ATC220220(ClsMiddleGroup_TpBase):
    MIDDLE_GROUP_NAME = "ATC220220"

    @classmethod
    def startup__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True


# =====================================================================================================================

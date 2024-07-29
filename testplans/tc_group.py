import time
from testplans import *
from funcs_aux import *
from classes_aux import *


# =====================================================================================================================
class ClsMiddleGroup_TpBase(ClsMiddleGroup):
    @classmethod
    def startup__group(cls) -> TYPE__RESULT_W_EXX:
        try:
            result = cls.startup__group__wrapped()
            if isinstance(result, Valid):
                result.run__if_not_finished()
        except Exception as exx:
            result = exx
        print(f"result__startup_group={result}")
        cls.result__startup_group = result
        return result

    @classmethod
    def teardown__group(cls) -> TYPE__RESULT_W_EXX:
        try:
            result = cls.teardown__group__wrapped()
            if isinstance(result, Valid):
                result.run__if_not_finished()
        except Exception as exx:
            result = exx
        print(f"result__teardown_group={result}")
        cls.result__teardown_group = result
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def startup__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True


# =====================================================================================================================

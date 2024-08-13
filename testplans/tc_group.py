from typing import *
from funcs_aux import *
from classes_aux import *

from .types import TYPE__RESULT_BASE, TYPE__RESULT_W_NORETURN, TYPE__RESULT_W_EXX


# =====================================================================================================================
class ClsMiddleGroup_TpBase(ClsMiddleGroup):
    MIDDLE_GROUP__CMP_METH = ["startup__group__wrapped", "teardown__group__wrapped"]

    result__startup_group: TYPE__RESULT_BASE = None
    result__teardown_group: TYPE__RESULT_BASE = None

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def clear__group(cls):
        # FIXME: need correct exit/terminate group
        cls.result__startup_group = None
        cls.result__teardown_group = None

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def startup__group(cls) -> TYPE__RESULT_W_EXX:
        result_link = cls.startup__group__wrapped

        result = Valid.get_result_or_exx(result_link)
        if isinstance(result, Valid):
            result.run__if_not_finished()

        print(f"result__startup_group={result}")
        cls.result__startup_group = result
        return result

    @classmethod
    def teardown__group(cls) -> TYPE__RESULT_W_EXX:
        result_link = cls.teardown__group__wrapped

        result = Valid.get_result_or_exx(result_link)
        if isinstance(result, Valid):
            result.run__if_not_finished()

        print(f"result__teardown_group={result}")
        cls.result__teardown_group = result
        return result

    # -----------------------------------------------------------------------------------------------------------------
    @classmethod
    def startup__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        pass

    @classmethod
    def teardown__group__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        pass


# =====================================================================================================================

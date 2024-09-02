from typing import *
from funcs_aux import *
from classes_aux import *

from .types import TYPE__RESULT_BASE, TYPE__RESULT_W_NORETURN, TYPE__RESULT_W_EXX


# =====================================================================================================================
class TcGroup_Base:
    """
    make groups by separating startup/teardown

    groups compare only by startup__cls__wrapped

    NOTE: try not to use (its not wrong but is incorrect)
        1. same startups with different teardowns!
        2. copyPasted startups/teardowns
    """
    @classmethod
    def group__check_equel(cls, other: Type[Self]) -> bool:
        try:
            return cls.startup__cls__wrapped is other.startup__cls__wrapped and cls.teardown__cls__wrapped is other.teardown__cls__wrapped
        except:
            pass
        return False

    @classmethod
    def startup__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True

    @classmethod
    def teardown__cls__wrapped(cls) -> TYPE__RESULT_W_NORETURN:
        return True


# =====================================================================================================================

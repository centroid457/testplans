from typing import *


# =====================================================================================================================
class TpResults:
    """
    Results for whole testplan at one dut!!!
    """
    TCS: List[Any]

    def __init__(self, tc: Any):
        pass
        self.TC = tc

    @classmethod
    def set__tcs(cls, tcs=None):
        cls.TCS = tcs
        for tc in tcs:
            pass

    def clear(self, cls=None):
        pass

    def add_result(self, cls, result):
        pass

    def get_result(self, cls):
        pass


# =====================================================================================================================

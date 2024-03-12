from typing import *


# =====================================================================================================================
class TpResults:
    """
    Results for whole testplan at one dut!!!
    """
    TCS: Dict[Type['TC'], List['TC']]

    def __init__(self, tc: 'TC'):
        pass
        self.TC = tc

    @classmethod
    def set__tcs(cls, tcs):
        for tc in tcs:
            cls.TCS.update({tc: []})

    def clear(self, cls=None):
        pass

    def add_result(self, cls, result):
        pass

    def get_result(self, cls):
        pass


# =====================================================================================================================

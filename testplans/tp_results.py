from typing import *


class TpResults:
    """
    Results for whole testplan at one dut!!!
    """
    TCS: Any

    def __init__(self, tcs: Iterable):
        pass

    def clear(self, cls=None):
        pass

    def add_result(self, cls, result):
        pass

    def get_result(self, cls):
        pass



from typing import *

from testplans import DutBase


class Device(DutBase):
    def __init__(self, value: Any):
        self.VALUE = value

    def check_present(self) -> bool:
        return True

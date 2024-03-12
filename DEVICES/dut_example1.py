from typing import *

from testplans import DutBase


class Device(DutBase):
    @property
    def VALUE(self) -> bool:
        return self.INDEX % 2 == 0


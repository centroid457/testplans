import time
from testplans import TestCaseBase
from . import tc1_direct


class TestCase(tc1_direct.TestCase):
    DESCRIPTION = "copy1"

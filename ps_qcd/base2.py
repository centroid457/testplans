from typing import *
import abc

from threading_manager import ThreadsManager


# =====================================================================================================================
class _Base:
    DUTS: List[Any] = None
    DESCRIPTION: str = ""
    PROGRESS: int = 0

    def __init__(self, duts: List[Any]):
        self.DUTS = duts

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    def startup(self) -> bool:
        self.PROGRESS = 1
        return True

    def teardown(self):
        self.PROGRESS = 100

    def dump_results(self):
        pass


# =====================================================================================================================
class TestCase(_Base, abc.ABC):
    def run(self) -> None:
        self.tc_step1()
        self.tc_step2()

    # -----------------------------------------------------------------------------------------------------------------
    def tc_step1(self, parallel: Optional[bool] = None) -> None:
        ThreadsManager().thread_items__clear()
        for dut in self.DUTS:
            ThreadsManager().decorator__to_thread(dut.func)(nothread=not parallel)
        ThreadsManager().wait_all()


# =====================================================================================================================

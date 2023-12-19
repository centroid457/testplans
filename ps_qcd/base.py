from typing import *
import abc

from threading_manager import ThreadsManager


# =====================================================================================================================
"""
мысли
===TC
СТРУКТУРА ДОЛЖНА БЫТЬ СТРОГОЙ!!!
1. должны быть либо зависимыми либо независимыми!
    - при работе с независимыми - все стартапы и проверки - полностью повторяются!
    - для зависимых - должны быть разделены шаги 
2.
    
===TP
    - запускает ТС в зависимости от параллельного запуска!

===КТО ДОЛЖЕН УПРАВЛЯТЬ ПАРАЛЛЕТЬНОСТЬЮ? ТС или TP???
"""


TP_RESULTS: str = "TP_RESULTS"


# =====================================================================================================================
class TestCase(abc.ABC):
    SKIP: Optional[bool] = None
    details: Dict[str, Any] = None
    result: Optional[bool] = None
    PARALLEL: Optional[bool] = True

    DUT: Any = None
    DESCRIPTION: str = ""
    PROGRESS: int = 0
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    def __init__(self, dut: Any):
        self.details = {}
        self.DUT = dut

    @classmethod
    @property
    def name(cls):
        return cls.__name__

    @classmethod
    def startup_all(cls) -> bool:
        """before batch work
        """
        return True

    def startup(self) -> bool:
        self.PROGRESS = 1
        return True

    def teardown(self):
        self.PROGRESS = 100

    @classmethod
    def teardown_all(cls):
        pass

    def dump_results(self):
        pass

    def run(self) -> None:
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()

    def add_details(self, details: Dict[str, Any]) -> None:
        self.details.update(details)

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================
class DutWithTp:
    PRESENT: Optional[bool] = None
    TP_RESULTS: Dict[Type[TestCase], TestCase] = None   # dict is convenient!!!

    check_present: Callable[..., bool]

    def mark_present(self) -> None:
        self.PRESENT = self.check_present()

    def check_result_final(self) -> Optional[bool]:
        for tc in self.TP_RESULTS.values():
            if not tc.SKIP:
                if not tc.result:
                    return tc.result
        return True


# =====================================================================================================================
class ManagerTp(abc.ABC):
    TCS: Dict[Type[TestCase], Optional[bool]] = {
        # TC1: True,
        # TC2: True
    }
    DUTS: List[DutWithTp] = [
        # Dut1,
        # Dut2
    ]

    def __init__(self):
        self.TCS_apply_skipped()

        self.duts_generate()
        self.duts_mark_presented()
        self.duts_results_init()

    # TCS -----------------------------------------------------------
    def TCS_apply_skipped(self):
        for tc, using in self.TCS.items():
            tc.SKIP = not using

    # DUTS -----------------------------------------------------------
    @abc.abstractmethod
    def duts_generate(self) -> None:
        pass

    def duts_mark_presented(self) -> None:
        for dut in self.DUTS:
            dut.mark_present()

    def duts_results_init(self) -> None:
        for dut in self.DUTS:
            dut.TP_RESULTS = dict()
            for tc in self.TCS:
                dut.TP_RESULTS.update({tc: tc(dut)})

    # RUN -----------------------------------------------------------
    def run(self) -> None:
        for tc in self.TCS:
            if tc.SKIP:
                continue
            if not tc.startup_all():
                continue

            ThreadsManager().thread_items__clear()
            for dut in self.DUTS:
                if dut.PRESENT:
                    ThreadsManager().decorator__to_thread(dut.TP_RESULTS[tc].run)(nothread=not tc.PARALLEL)
            ThreadsManager().wait_all()
            tc.teardown_all()


# =====================================================================================================================

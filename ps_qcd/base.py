from typing import *
import abc

from threading_manager import ThreadsManager


# =====================================================================================================================
"""
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


# =====================================================================================================================
class _Base:
    DUT: Any = None
    DESCRIPTION: str = ""
    PROGRESS: int = 0
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    def __init__(self, dut: Any):
        self.DUT = dut

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
    details: Dict[str, Any] = {}
    result: Optional[bool] = None
    PARALLEL: Optional[bool] = True
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL
    # TODO: FINISH PARALLEL

    def run(self) -> None:
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()
    #
    # def add_details(self, details: Dict[str, Any]) -> None:
    #     self.details.update(details)
    #
    # def dump_results(self):
    #     print(f"{self.name}: result={self.result}")
    #     for name, value in self.details.items():
    #         print(f"\t|{name}: {value}")
    #         for name2, value2 in value.details.items():
    #             print(f"\t\t|{name2}: {value2}")

    # -----------------------------------------------------------------------------------------------------------------
    @abc.abstractmethod
    def run_wrapped(self) -> bool:
        pass


# =====================================================================================================================
# class TestCase(_Base):
#     details: Dict[Type[TestCaseStep], Union[bool, TestCaseStep]] = {
#         # TCS1: True,
#         # TCS2: True
#     }
#
#     @property
#     def result(self) -> bool:
#         for detail in self.details.values():
#             if detail in [False, None]:
#                 continue
#             if not detail.result:
#                 return False
#         return True
#
#     def run(self) -> None:
#         if self.startup():
#             for detail, start in self.details.items():
#                 if start:
#                     self.details[detail] = detail(self.duts)
#                     self.details[detail].run()
#                     if self.details[detail].STOP_IF_FALSE_RESULT and not self.details[detail].result:
#                         break
#         self.teardown()
#
#     # ---------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class TestPlan(_Base):
    tcs: Dict[Type[TestCase], Union[None, bool, TestCase]] = {
        # TC1: True,
        # TC2: True
    }

    # @property
    # def result(self) -> bool:
    #     for tc in self.tcs.values():
    #         if tc in [False, None]:
    #             continue
    #         if not tc.result:
    #             return False
    #     return True
    #
    # def run(self) -> None:
    #     if not self.DUT.check_present():
    #         return
    #
    #     if self.startup():
    #         for tc, start in self.tcs.items():
    #             if start:
    #                 self.tcs[tc] = tc(self.DUT)
    #                 self.tcs[tc].run()
    #                 if self.tcs[tc].STOP_IF_FALSE_RESULT and not self.tcs[tc].result:
    #                     break
    #     self.teardown()
    #
    # def dump_results(self):
    #     print("=" * 80)
    #     for tc, tc_object in self.tcs.items():
    #         if tc_object:
    #             # print(f"{tc_object.name}:result={tc_object.result}")
    #             tc_object.dump_results()
    #     print("="*80)

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class ManagerTp(abc.ABC):
    TP: TestPlan = TestPlan
    DUTS: Dict[Any, bool] = {
        # Dut1: None,
        # Dut2: None,
    }

    def __init__(self):
        self.duts_generate()
        self.duts_mark_presented()

    @abc.abstractmethod
    def duts_generate(self) -> None:
        pass

    def duts_mark_presented(self) -> None:
        for dut in self.DUTS:
            self.DUTS[dut] = dut.check_present()

    def run(self) -> None:
        for tc in self.TP.tcs:
            ThreadsManager().thread_items__clear()
            for dut, present in self.DUTS.items():
                if present:
                    ThreadsManager().decorator__to_thread(tc(dut).run)(nothread=not tc.PARALLEL)
            ThreadsManager().wait_all()


# =====================================================================================================================

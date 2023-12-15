from typing import *


# =====================================================================================================================
class _Base:
    details: Dict
    result: bool
    is_testcase: Optional[bool] = None

    DUT: Any = None
    DESCRIPTION: str = ""
    PROGRESS: int = 0
    STOP_IF_FALSE_RESULT: Optional[bool] = None

    def __init__(self, DUT: Any):
        self.DUT = DUT

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
        if self.is_testcase:
            print(f"\t{self.name}: result={self.result}")
            for name, value in self.details.items():
                print(f"\t\t|{name}: {value}")
        else:
            print("=" * 80)
            for tc, tc_object in self.details.items():
                if tc_object:
                    print(f"{tc_object.name}:result={tc_object.result}")
                    tc_object.dump_results()
            print("="*80)


# =====================================================================================================================
class TestCase(_Base):
    details: Dict[str, Any] = {}
    result: Optional[bool] = None

    is_testcase = True

    def run(self) -> None:
        if self.startup():
            self.result = self.run_wrapped()
        self.teardown()

    def add_details(self, details: Dict[str, Any]) -> None:
        self.details.update(details)

    # -----------------------------------------------------------------------------------------------------------------
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
#                     self.details[detail] = detail(self.DUT)
#                     self.details[detail].run()
#                     if self.details[detail].STOP_IF_FALSE_RESULT and not self.details[detail].result:
#                         break
#         self.teardown()
#
#     # ---------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class TestPlan(_Base):
    details: Dict[Type[TestCase], Union[bool, TestCase]] = {
        # TC1: True,
        # TC2: True
    }

    @property
    def result(self) -> bool:
        for detail in self.details.values():
            if detail in [False, None]:
                continue
            if not detail.result:
                return False
        return True

    def run(self) -> None:
        if not self.DUT.check_present():
            return

        if self.startup():
            for detail, start in self.details.items():
                if start:
                    self.details[detail] = detail(self.DUT)
                    self.details[detail].run()
                    if self.details[detail].STOP_IF_FALSE_RESULT and not self.details[detail].result:
                        break
        self.teardown()

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================

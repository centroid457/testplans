from typing import *
import abc


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

    def add_details(self, details: Dict[str, Any]) -> None:
        self.details.update(details)

    def dump_results(self):
        print(f"{self.name}: result={self.result}")
        for name, value in self.details.items():
            print(f"\t|{name}: {value}")
            for name2, value2 in value.details.items():
                print(f"\t\t|{name2}: {value2}")

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
#                     self.details[detail] = detail(self.dut)
#                     self.details[detail].run()
#                     if self.details[detail].STOP_IF_FALSE_RESULT and not self.details[detail].result:
#                         break
#         self.teardown()
#
#     # ---------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class TestPlan(_Base):
    tcs: Dict[Type[TestCase], Union[bool, TestCase]] = {
        # TC1: True,
        # TC2: True
    }

    @property
    def result(self) -> bool:
        for detail in self.tcs.values():
            if detail in [False, None]:
                continue
            if not detail.result:
                return False
        return True

    def run(self) -> None:
        if not self.DUT.check_present():
            return

        if self.startup():
            for detail, start in self.tcs.items():
                if start:
                    self.tcs[detail] = detail(self.DUT)
                    self.tcs[detail].run()
                    if self.tcs[detail].STOP_IF_FALSE_RESULT and not self.tcs[detail].result:
                        break
        self.teardown()

    def dump_results(self):
        print("=" * 80)
        for tc, tc_object in self.tcs.items():
            if tc_object:
                # print(f"{tc_object.name}:result={tc_object.result}")
                tc_object.dump_results()
        print("="*80)

    # -----------------------------------------------------------------------------------------------------------------


# =====================================================================================================================
class ManagerTp(abc.ABC):
    TPs: Dict[TestPlan, Any] = {
        # TpDut1: None,
        # TpDut2: None,
    }

    def __init__(self):
        self.tps_generate()

    @abc.abstractmethod
    def tps_generate(self) -> None:
        pass

    def tps_presented(self) -> List[TestPlan]:
        result = []
        for tp in self.TPs:
            if tp.DUT.check_present():
                result.append(tp)
        return result

    def run(self) -> None:
        if not self.tps_presented():
            return

        for tc in self.tps_presented()[0].tcs:
            if tc.PARALLEL:
                for tp in self.tps_presented():
                    # if tp.
                    pass





            for detail, start in self.tcs.items():
                if start:
                    self.tcs[detail] = detail(self.DUT)
                    self.tcs[detail].run()
                    if self.tcs[detail].STOP_IF_FALSE_RESULT and not self.tcs[detail].result:
                        break
        self.teardown()

# =====================================================================================================================

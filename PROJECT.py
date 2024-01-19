from typing import *


# =====================================================================================================================
class PROJECT:
    # AUX --------------------------------------------------
    _VERSION_TEMPLATE: Tuple[int] = (0, 0, 2)

    # AUTHOR -----------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # PROJECT ----------------------------------------------
    NAME_IMPORT: str = "testplans"
    NAME_INSTALL: str = NAME_IMPORT.replace("_", "-")
    KEYWORDS: List[str] = [
        "testplan",
        "testplan structure framework",
        "testplan gui",
        "testplan multy dut",
        "testplan several dut",
    ]
    CLASSIFIERS_TOPICS_ADD: List[str] = [
        # "Topic :: Communications",
        # "Topic :: Communications :: Email",
    ]

    # README -----------------------------------------------
    # add DOUBLE SPACE at the end of all lines! for correct representation in MD-viewers
    DESCRIPTION_SHORT: str = "simple testplan framework for several DUTs"
    DESCRIPTION_LONG: str = """designed to apply testplan for several DUTs"""
    FEATURES: List[str] = [
        # "feat1",
        # ["feat2", "block1", "block2"],

        "thread safe",
        "safe stop process",
        ["skip", "tc", "tc on dut", "dut"],
    ]

    # HISTORY -----------------------------------------------
    VERSION: Tuple[int, int, int] = (0, 0, 2)
    VERSION_STR: str = ".".join(map(str, VERSION))
    TODO: List[str] = [
        "add meta for settings in tcs, it is better then applying in manually in TP!"
    ]
    FIXME: List[str] = [
        "..."
    ]
    NEWS: List[str] = [
        "fix exx without settings",
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================

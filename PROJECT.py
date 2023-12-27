from typing import *


# =====================================================================================================================
class PROJECT:
    # MAIN -------------------------------------------------
    AUTHOR_NAME: str = "Andrei Starichenko"
    AUTHOR_EMAIL: str = "centroid@mail.ru"
    AUTHOR_HOMEPAGE: str = "https://github.com/centroid457/"

    # ------------------------------------------------------
    NAME_INSTALL: str = "prj-name"
    NAME_IMPORT: str = "prj_name"
    KEYWORDS: List[str] = [
        "kw1",
    ]

    DESCRIPTION_SHORT: str = "descr short (git/prg descr)"
    DESCRIPTION_LONG: str = "designed for ..."
    FEATURES: List[str] = [
        "feat1",
        "feat2",
        ["feat3", "block1", "block2"],
        "feat4",
    ]
    WISHES: List[str] = [
        "add ..."
    ]

    # NEW VERSION -------------------------------------------
    VERSION: str = "0.0.1"
    NEWS: List[str] = [
        "add ..."
    ]


# =====================================================================================================================
if __name__ == '__main__':
    pass


# =====================================================================================================================

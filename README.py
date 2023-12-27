import pathlib
from typing import *

from PROJECT import PROJECT


# =====================================================================================================================
class Readme:
    # ------------------------------------------------
    FILE_NAME: str = "README.md"
    filepath: pathlib.Path = pathlib.Path(FILE_NAME)

    DIR_NAME: str = "EXAMPLES"
    dirpath: pathlib.Path = pathlib.Path(DIR_NAME)

    # ------------------------------------------------
    SEPARATOR_PATTERN = r'(\**\n+)*## USAGE EXAMPLES'

    LINE_STARS_WRAPPER: str = "*" * 80
    LINE_STARS_FILE_SEPARATOR: str = "*" * 30
    LINE_FILE_HEADER: str = "```python"
    LINE_FILE_FOOTER: str = "```"
    LINE_SEPARATOR_FILE: str = LINE_STARS_FILE_SEPARATOR

    LINES_EXAMPLES_START: List[str] = [
        f"",
        f"",
        LINE_STARS_WRAPPER,
        f"## USAGE EXAMPLES",
        f"See tests and sourcecode for other examples.",
    ]

    # WORK WRITE ------------------------------------------------------------------------------------------------------
    @classmethod
    def file_clear(cls) -> None:
        cls.filepath.write_text("")

    @classmethod
    def file_append_lines(cls, lines: Optional[Union[str, List[str]]] = None) -> None:
        if not lines:
            lines = ""
        if isinstance(lines, str):
            lines = [lines, ]
        with cls.filepath.open("a") as fo_append:
            for lines in lines:
                fo_append.write(f"{lines}\n")

    # GENERATE ========================================================================================================
    @classmethod
    def autogenerate(cls):
        cls.file_clear()
        cls.append_main()
        cls.append_examples()

    @classmethod
    def append_main(cls):
        FEATURES = [
            f"",
            f"",
            f"## Features",
        ]
        for num, feature in enumerate(PROJECT.FEATURES, start=1):
            if isinstance(feature, list):
                FEATURES.append(f"{num}. {feature[0]}:  ")
                for block in feature[1:]:
                    FEATURES.append(f"\t- {block}  ")
            else:
                FEATURES.append(f"{num}. {feature}  ")

        LINES = [
            f"# {PROJECT.NAME_IMPORT}",
            f"{PROJECT.DESCRIPTION_SHORT.capitalize()}.  ",
            f"{PROJECT.DESCRIPTION_LONG.capitalize()}.  ",

            *FEATURES,

            f"",
            f"",
            cls.LINE_STARS_WRAPPER,
            f"## License",
            f"See the [LICENSE](LICENSE) file for license rights and limitations (MIT).",

            f"",
            f"",
            f"## Release history",
            f"See the [HISTORY.md](HISTORY.md) file for release history.",

            f"",
            f"",
            f"## Installation",
            f"```commandline",
            f"pip install {PROJECT.NAME_INSTALL}",
            f"```",

            f"",
            f"",
            f"## Import",
            f"```python",
            f"from {PROJECT.NAME_IMPORT} import *",
            f"```",
        ]
        cls.file_append_lines(LINES)

    @classmethod
    def append_examples(cls):
        """
        NOTE: don't skip none-python files! it could be as part of examples! just name it in appropriate way!
        """
        cls.file_append_lines(cls.LINES_EXAMPLES_START)
        cls.file_append_lines()

        files = [item for item in cls.dirpath.iterdir() if item.is_file()]

        for index, file in enumerate(files, start=1):
            LINES = [
                cls.LINE_SEPARATOR_FILE,
                f"### {index}. {file.name}",
                cls.LINE_FILE_HEADER,
                file.read_text().strip(),
                cls.LINE_FILE_FOOTER,
                f"",
            ]
            cls.file_append_lines(LINES)

        cls.file_append_lines(cls.LINE_STARS_WRAPPER)


# =====================================================================================================================
if __name__ == '__main__':
    Readme.autogenerate()


# =====================================================================================================================

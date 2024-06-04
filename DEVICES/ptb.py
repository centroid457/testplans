from typing import *
from testplans import DutBase
from bus_user import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid, DutBase):
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    EOL__SEND = b"\n"

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX}:"

    def address__answer_validation(self) -> bool:
        result = self.write_read__last_validate("get name", f"PTB", prefix="*:") and self.write_read__last_validate("get addr", [f"{self.INDEX}", f"0{self.INDEX}"], prefix="*:")
        return result

    def __init__(self, index: int, **kwargs):
        if index is not None:
            self.INDEX = index
        super().__init__(**kwargs)

    @property
    def VALUE(self) -> bool:
        return self.INDEX % 2 == 0


# =====================================================================================================================
if __name__ == "__main__":
    pass

    # emu = Ptb_Emulator()
    # emu.start()
    # emu.wait()

    # dev = Device()
    # print(f"{dev.connect()=}")
    # print(f"{dev.ADDRESS=}")


# =====================================================================================================================

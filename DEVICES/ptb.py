from typing import *
from testplans import DeviceBase
from bus_user import *


# =====================================================================================================================
class Ptb_SerialClient(SerialClient_FirstFree_AnswerValid):
    LOG_ENABLE = True
    RAISE_CONNECT = False
    INDEX: int | None

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX}:"

    def address__answer_validation(self) -> bool:
        result = self.write_read__last_validate("get name", f"PTB") and self.write_read__last_validate("get addr", [f"{self.INDEX}", f"0{self.INDEX}"])
        return result


# =====================================================================================================================
class Device(DeviceBase):
    conn = Ptb_SerialClient()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.conn.INDEX = self.INDEX


# =====================================================================================================================
if __name__ == "__main__":
    pass

    # emu = Ptb_Emulator()
    # emu.start()
    # emu.wait()

    dev = Ptb_SerialClient()
    print(f"{dev.connect()=}")
    print(f"{dev.ADDRESS=}")


# =====================================================================================================================

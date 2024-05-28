from typing import *
from testplans import DeviceBase
from bus_user import *


# =====================================================================================================================
class Ptb_SerialClient(SerialClient):
    # ADDRESS = AddressAutoAcceptVariant.FIRST_FREE__PAIRED_FOR_EMU
    ADDRESS = Type__AddressAutoAcceptVariant.FIRST_FREE__ANSWER_VALID
    RAISE_CONNECT = False

    INDEX: int | None

    # EMULATOR ------------------------
    # _EMULATOR__CLS = Ptb_Emulator
    # _EMULATOR__START = True

    @property
    def PREFIX(self) -> str:
        return f"PTB:{self.INDEX}:"

    def address__answer_validation(self) -> bool:
        return self.write_read_line_last("get name") == f"PTB {self.INDEX}"


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

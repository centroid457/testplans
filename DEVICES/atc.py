from typing import *
from bus_user import *


# =====================================================================================================================
class Device(SerialClient_FirstFree_AnswerValid):
    LOG_ENABLE = True
    RAISE_CONNECT = False
    BAUDRATE = 115200
    PREFIX = "ATC:03:"
    EOL__SEND = b"\r"

    def address__answer_validation(self) -> bool:
        return self.write_read__last_validate("get name", "ATC 03", prefix=self.PREFIX)


# =====================================================================================================================
if __name__ == "__main__":
    pass

    # emu = Atc_Emulator()
    # emu.start()
    # emu.wait()

    dev = Device()
    print(f"{dev.connect()=}")
    # print(f"{dev.addresses_system__detect()=}")
    print(f"{dev.ADDRESS=}")
    #
    # print(f"{dev.address__answer_validation()=}")
    # print(f"{dev.address__answer_validation()=}")
    # print(f"{dev.address__answer_validation()=}")
    #
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.write_read_line_last('get name')=}")
    # print(f"{dev.disconnect()=}")
    # print(f"{dev.ADDRESS=}")


# =====================================================================================================================

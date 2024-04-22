from typing import *
from pydantic import BaseModel


# =====================================================================================================================
class ModelStand(BaseModel):
    name: str           # "Stand PSU"
    description: str    # "test PSU for QCD"
    sn: str


class ModelDevice(BaseModel):
    name: str           # "PSU"
    description: str    # "Power Supply Unit"
    sn: str

    index: int          # device position in stand???


class ModelTcClsInfo(BaseModel):
    name: str
    description: str

    is_async: bool = False
    is_skipped: bool = False

    settings: dict[str, Any] = {
        # CONTENT IS NOT SPECIFIED!
        # "ANY_1": Any,
    }

class ModelTcInstResult(ModelTcClsInfo):
    DEVICE: ModelDevice

    timestamp: float
    is_active: bool = False
    is_async: bool = False
    is_skipped: bool = False

    progress: int = 0
    result: bool | None = None

    details: dict[str , Any] = {
        # CONTENT IS NOT SPECIFIED!
        # "ANY_2": Any,
    }


class ModelSendResult(ModelTcInstResult):
    STAND: ModelStand


class ModelTpInfo(BaseModel):
    STAND: ModelStand
    TESTCASES: list[ModelTcClsInfo]


class ModelTpResults(BaseModel):
    STAND: ModelStand
    TESTCASES: list[list[ModelTcInstResult]]


# =====================================================================================================================

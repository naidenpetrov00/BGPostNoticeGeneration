from enum import Enum


class Offices(Enum):
    NEDELCHO = "841"
    STRAMSKI = "870"
    ROSEN = "910"


class Mode(str, Enum):
    SINGLE = "single"
    PAIR = "pair"

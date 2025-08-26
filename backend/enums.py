from enum import Enum


class Offices(Enum):
    NEDELCHO = "841"
    STRAMSKI = "870"
    ROSEN = "910"


class PairMode(str, Enum):
    single = "single"
    pair = "pair"
    compact = "compact"

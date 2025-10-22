from dataclasses import dataclass
from pathlib import Path

from enums import Offices


@dataclass(frozen=True)
class Paths:
    blank_template: Path
    envelope_template: Path
    envelope_template_870: Path
    envelope_template_910: Path
    notices_dir: Path
    envelopes_dir: Path
    static: Path


paths = Paths(
    blank_template=Path("./blanks/243_form_bigger_field_v7.pdf"),
    envelope_template=Path("./blanks/Letter_C5_v3.pdf"),
    envelope_template_870=Path("./blanks/Letter870.pdf"),
    envelope_template_910=Path("./blanks/Letter910.pdf"),
    notices_dir=Path("./notices"),
    envelopes_dir=Path("./envelopes"),
    static=Path("./static"),
)


def getEnvelopePath(office):
    if office == Offices.NEDELCHO.value:
        return paths.envelope_template
    elif office == Offices.STRAMSKI.value:
        return paths.envelope_template_870
    elif office == Offices.ROSEN.value:
        return paths.envelope_template_910

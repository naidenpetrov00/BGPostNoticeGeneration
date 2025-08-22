from dataclasses import dataclass
from pathlib import Path

@dataclass(frozen=True)
class Paths:
    blank_template: Path
    envelope_template: Path
    notices_dir: Path
    envelopes_dir: Path
    static: Path

paths = Paths(
        blank_template=Path("./blanks/243_form_test_fonts_v6.pdf"),
        envelope_template=Path("./blanks/Letter_C5_v3.pdf"),
        notices_dir=Path("./notices"),
        envelopes_dir=Path("./envelopes"),
        static=Path("./static")
    )
from pathlib import Path


class Paths:
    blank_template: Path
    envelope_template: Path
    notices_dir: Path
    envelopes_dir: Path

paths = Paths(
        blank_template=Path("./blanks/243_Open_Sans_v2.pdf"),
        envelope_template=Path("./blanks/Letter_C5_v3.pdf"),
        notices_dir=Path("./notices"),
        envelopes_dir=Path("./envelopes"),
    )
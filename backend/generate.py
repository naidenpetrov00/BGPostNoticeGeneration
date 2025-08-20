from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging
import pandas as pd
from pandas import Series
from pypdf import PdfReader, PdfWriter
from datetime import datetime
from zoneinfo import ZoneInfo

from utils import (
    log_the_last_number,
    merge_pdfs,
    regen_appearances_batch,
    write_to_pdf,
)
from barcode import BarCode
from envelopeField import EnvelopeField
from blankField import BlankFields
import readData

LOG = logging.getLogger(__name__)

class Mode(str, Enum):
    SINGLE = "single"
    PAIR = "pair"

@dataclass(frozen=True)
class Paths:
    blank_template: Path
    envelope_template: Path
    notices_dir: Path
    envelopes_dir: Path

@dataclass
class GenerateResult:
    notices_merged: Path
    envelopes_merged: Path
    protocol_excel: Path

def _now_sofia_str() -> str:
    # For filenames (safe) and display (keep both if you want)
    return datetime.now(ZoneInfo("Europe/Sofia")).strftime("%Y-%m-%d_%H-%M-%S")

def _ensure_dirs(paths: Paths) -> None:
    paths.notices_dir.mkdir(parents=True, exist_ok=True)
    paths.envelopes_dir.mkdir(parents=True, exist_ok=True)

def _new_writers(blank_reader: PdfReader, env_reader: PdfReader) -> Tuple[PdfWriter, PdfWriter]:
    notice = PdfWriter(); notice.append(blank_reader)
    env = PdfWriter(); env.append(env_reader)
    return notice, env

def _row_has_address(row: Series) -> bool:
    val = row.get(readData.adressProp)  # keep external name but treat as "address"
    return isinstance(val, str) and val.strip() != ""

def _protocol_row(row: Series, barcode: BarCode, address_first_line: str) -> Dict[str, str]:
    number = "Товарителница"
    date_prop = "Дата"
    return {
        readData.documentNumber: row[readData.documentNumber],
        readData.recieverProp: row[readData.recieverProp],
        readData.adressProp: address_first_line,
        readData.outDate: row[readData.outDate],
        number: barcode.get_barcode_text(),
        # sender & date are added once outside into row 0/metadata if you prefer
    }

def generate_notice(file: pd.DataFrame, mode: Mode = Mode.SINGLE) -> GenerateResult:
    paths = Paths(
        blank_template=Path("./blanks/243_Open_Sans_v2.pdf"),
        envelope_template=Path("./blanks/Letter_C5_v3.pdf"),
        notices_dir=Path("./notices"),
        envelopes_dir=Path("./envelopes"),
    )
    _ensure_dirs(paths)

    # Preload templates once
    blank_reader = PdfReader(str(paths.blank_template))
    env_reader = PdfReader(str(paths.envelope_template))

    # Setup field providers
    blank_fields = BlankFields()
    envelope_fields = EnvelopeField()

    # Build protocol rows in memory
    protocol_rows: List[Dict[str, str]] = []

    # Prepare output tracking
    notice_paths: List[str] = []
    envelope_paths: List[str] = []

    timestamp = _now_sofia_str()
    sender_col = readData.sender
    date_col = "Дата"
    number_col = "Товарителница"

    # Metadata first row (optional)
    protocol_header = {
        sender_col: getattr(blank_fields, "sender", ""),
        date_col: datetime.now(ZoneInfo("Europe/Sofia")).strftime("%d.%m.%Y %H:%M:%S"),
    }

    prev_pair_doc_number: Optional[str] = None
    pending_row_for_pair: Optional[Series] = None

    for i, (index, row) in enumerate(file.iterrows()):
        if not _row_has_address(row):
            LOG.warning("Missing address for case=%s doc=%s",
                        row.get(readData.caseNumberProp), row.get(readData.documentNumber))
            continue

        # File paths
        case_number = row[readData.caseNumberProp]
        out_notice = paths.notices_dir / f"{index}_{case_number}.pdf"
        out_env = paths.envelopes_dir / f"{index}_{case_number}_envelope.pdf"

        # Pair logic
        if mode == Mode.PAIR:
            if pending_row_for_pair is None:
                pending_row_for_pair = row
                prev_pair_doc_number = row[readData.documentNumber]
                continue
            else:
                # We have a pair: use current row + previous document number
                curr = row
                barcode = BarCode()

                notice_w, env_w = _new_writers(blank_reader, env_reader)
                notice_w.update_page_form_field_values(
                    notice_w.pages[0],
                    blank_fields.getFieldValues(curr, barcode, prev_pair_doc_number),
                    auto_regenerate=False,
                )
                env_w.update_page_form_field_values(
                    env_w.pages[0],
                    envelope_fields.getFieldValues(curr, barcode),
                    auto_regenerate=False,
                )

                write_to_pdf(notice_w, str(out_notice))
                write_to_pdf(env_w, str(out_env))
                notice_paths.append(str(out_notice.resolve()))
                envelope_paths.append(str(out_env.resolve()))

                addr_first = str(curr[readData.adressProp]).split(";")[0]
                protocol_rows.append(_protocol_row(curr, barcode, addr_first))

                # clear pair state
                pending_row_for_pair = None
                prev_pair_doc_number = None
        else:
            # SINGLE mode
            barcode = BarCode()
            notice_w, env_w = _new_writers(blank_reader, env_reader)
            notice_w.update_page_form_field_values(
                notice_w.pages[0],
                blank_fields.getFieldValues(row, barcode),
                auto_regenerate=False,
            )
            env_w.update_page_form_field_values(
                env_w.pages[0],
                envelope_fields.getFieldValues(row, barcode),
                auto_regenerate=False,
            )
            write_to_pdf(notice_w, str(out_notice))
            write_to_pdf(env_w, str(out_env))
            notice_paths.append(str(out_notice.resolve()))
            envelope_paths.append(str(out_env.resolve()))

            addr_first = str(row[readData.adressProp]).split(";")[0]
            protocol_rows.append(_protocol_row(row, barcode, addr_first))

    # Handle dangling first-of-pair
    if mode == Mode.PAIR and pending_row_for_pair is not None:
        LOG.warning("Odd number of rows – last item in PAIR mode had no partner: case=%s doc=%s",
                    pending_row_for_pair.get(readData.caseNumberProp),
                    pending_row_for_pair.get(readData.documentNumber))

    # Regenerate appearances after all writes
    # regen_appearances_batch(notice_paths + envelope_paths)

    # Merge outputs
    notices_merged = paths.notices_dir / f"notices_ALL_{timestamp}.pdf"
    envelopes_merged = paths.envelopes_dir / f"envelopes_ALL_{timestamp}.pdf"
    merge_pdfs(notice_paths, str(notices_merged))
    merge_pdfs(envelope_paths, str(envelopes_merged))

    # Protocol Excel
    # Put metadata in first row if desired:
    protocol_df = pd.DataFrame(protocol_rows)
    if protocol_header:
        # Make a first row with sender/date, keep columns consistent
        hdr = {c: "" for c in protocol_df.columns}
        hdr.update({sender_col: protocol_header.get(sender_col, ""),
                    date_col: protocol_header.get(date_col, "")})
        protocol_df = pd.concat([pd.DataFrame([hdr]), protocol_df], ignore_index=True)

    protocol_path = paths.notices_dir / f"noticesTable_{timestamp}.xlsx"
    protocol_df.to_excel(protocol_path, index=False)

    log_the_last_number()
    return GenerateResult(
        notices_merged=notices_merged,
        envelopes_merged=envelopes_merged,
        protocol_excel=protocol_path,
    )

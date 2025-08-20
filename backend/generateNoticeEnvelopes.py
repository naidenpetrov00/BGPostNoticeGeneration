import datetime as date
from pathlib import Path
from pandas import Series
import pandas as pd
from utils import (
    log_the_last_number,
    merge_pdfs,
    regen_appearances_batch,
    write_to_pdf,
)
from barcode import BarCode
from envelopeField import EnvelopeField
from blankField import BlankFields
from pypdf import PdfReader, PdfWriter
import readData

async def generateNotice(file,mode):

    # blank_path = "./blanks/243_Open_Sans_v2.pdf"
    # envelope_path = "./blanks/Letter_C5_v3.pdf"

    output_folder = "./notices"
    envelope_output_folder = "./envelopes"

    today_date = date.datetime.today().strftime("%d.%m.%Y %H:%M:%S")

    blank_fields = BlankFields()
    envelope_fields = EnvelopeField()

    number = "Товарителница"
    date_prop = "Дата"
    results_df = pd.DataFrame(
        columns=[
            readData.documentNumber,
            readData.recieverProp,
            readData.adressProp,
            number,
            readData.sender,
            date_prop,
            readData.outDate,
        ]
    )
    results_df.loc[1, readData.sender] = blank_fields.sender
    results_df.loc[1, date_prop] = today_date


    def updateTable(row: Series, barcode: BarCode):
        nonlocal results_df
        results_df = pd.concat(
            [
                results_df,
                pd.DataFrame(
                    [
                        {
                            readData.documentNumber: row[readData.documentNumber],
                            readData.recieverProp: row[readData.recieverProp],
                            readData.adressProp: row[readData.adressProp].split(";")[0],
                            readData.outDate: row[readData.outDate],
                            number: barcode.get_barcode_text(),
                        }
                    ]
                ),
            ],
            ignore_index=True,
        )


    prev_row_doc_number = None

    notice_paths: list[str] = []
    envelope_paths: list[str] = []
    for i, (index, row) in enumerate(file.iterrows()):
        adress = row[readData.adressProp]
        case_number = row[readData.caseNumberProp]
        document_number = row[readData.documentNumber]
        if pd.isna(adress):
            print(f"{case_number} : {document_number}")
            continue
        blank_reader = PdfReader(blank_path)
        envelope_reader = PdfReader(envelope_path)
        output_path = f"{output_folder}/{index}_{case_number}.pdf"
        output_envelope_path = (
            f"{envelope_output_folder}/{index}_{case_number}_envelope.pdf"
        )
        output_pdf = PdfWriter()
        output_envelope_pdf = PdfWriter()
        output_pdf.append(blank_reader)
        output_envelope_pdf.append(envelope_reader)
        if mode == "pair":
            if i % 2 == 0:
                prev_row_doc_number = document_number
            else:
                barcode = BarCode()
                output_pdf.update_page_form_field_values(
                    output_pdf.pages[0],
                    blank_fields.getFieldValues(row, barcode, prev_row_doc_number),
                    auto_regenerate=False,
                )
                output_envelope_pdf.update_page_form_field_values(
                    output_envelope_pdf.pages[0],
                    envelope_fields.getFieldValues(row, barcode),
                    auto_regenerate=False,
                )
                updateTable(row, barcode)
                write_to_pdf(output_pdf, output_path)
                notice_paths.append(str(Path(output_path).resolve()))
                write_to_pdf(output_envelope_pdf, output_envelope_path)
                envelope_paths.append(str(Path(output_envelope_path).resolve()))
        elif mode == "single":
            barcode = BarCode()
            output_pdf.update_page_form_field_values(
                output_pdf.pages[0],
                blank_fields.getFieldValues(row, barcode),
                auto_regenerate=False,
            )
            output_envelope_pdf.update_page_form_field_values(
                output_envelope_pdf.pages[0],
                envelope_fields.getFieldValues(row, barcode),
                auto_regenerate=False,
            )
            updateTable(row, barcode)
            write_to_pdf(output_pdf, output_path)
            notice_paths.append(str(Path(output_path).resolve()))
            write_to_pdf(output_envelope_pdf, output_envelope_path)
            envelope_paths.append(str(Path(output_envelope_path).resolve()))

    regen_appearances_batch(notice_paths + envelope_paths)

    notices_merged_path = f"{output_folder}/notices_ALL_{today_date}.pdf"
    merge_pdfs(notice_paths, notices_merged_path)

    # Merge all envelopes into one big PDF
    envelopes_merged_path = f"{envelope_output_folder}/envelopes_ALL_{today_date}.pdf"
    merge_pdfs(envelope_paths, envelopes_merged_path)

    log_the_last_number()
    protocol_path = f"{output_folder}/noticesTable{today_date}.xlsx"
    results_df.to_excel(protocol_path, index=False)

    return [notices_merged_path, envelopes_merged_path, protocol_path]
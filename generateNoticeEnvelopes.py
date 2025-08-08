import datetime as date
from pathlib import Path
from pandas import Series
import pandas as pd
from utils import (
    log_the_last_number,
    regen_appearances_batch,
    regenerate_pdf_appearance,
    write_to_pdf,
)
from barcode import BarCode
from envelopeField import EnvelopeField
from blankField import BlankFields
from readData import readExcelFiles
from pypdf import PdfReader, PdfWriter
from pypdf.generic import NameObject, BooleanObject, TextStringObject, DictionaryObject
import readData
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    "--mode",
    choices=["single", "pair"],
    help="Notise per row or notice per pair by case number",
)
args = parser.parse_args()

blank_path = "./blanks/243_Open_Sans_v2.pdf"
envelope_path = "./blanks/Letter_C5_v1.pdf"

output_folder = "./notices"
envelope_output_folder = "./envelopes"

today_date = date.datetime.today().strftime("%d.%m.%Y")

blank_fields = BlankFields()
envelope_fields = EnvelopeField()

files = readExcelFiles()

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
    global results_df
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

processed_paths = []

for file_df in files:
    for i, (index, row) in enumerate(file_df.iterrows()):
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

        if args.mode == "pair":
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
                processed_paths.append(str(Path(output_path).resolve()))
                # regenerate_pdf_appearance(output_path)
                write_to_pdf(output_envelope_pdf, output_envelope_path)
                processed_paths.append(str(Path(output_envelope_path).resolve()))
                # regenerate_pdf_appearance(output_envelope_path)

        elif args.mode == "single":
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
            processed_paths.append(str(Path(output_path).resolve()))
            # regenerate_pdf_appearance(output_path)
            write_to_pdf(output_envelope_pdf, output_envelope_path)
            processed_paths.append(str(Path(output_envelope_path).resolve()))
            # regenerate_pdf_appearance(output_envelope_path)

regen_appearances_batch(processed_paths)

log_the_last_number()
results_df.to_excel(f"{output_folder}/noticesTable{today_date}.xlsx", index=False)

import os
import pandas as pd
from pandas import DataFrame
from infrastructure.case_mapping import attach_case_ids
from config import (
    ALLOCATED_AMOUNT_COL,
    ALLOCATION_DATE_COL,
    CASE_NUMBER_COL,
    DOCUMENTS_FOLDER_PATH,
    PAYMENT_FOR_COL,
    RECEIVER_COL,
)


def read_documents() -> DataFrame:
    frames = []

    for filename in os.listdir(DOCUMENTS_FOLDER_PATH):
        file_path = os.path.join(DOCUMENTS_FOLDER_PATH, filename)
        print(f"Processing file: {filename}")
        df = pd.read_excel(file_path, dtype={CASE_NUMBER_COL: "string"})

        cleaned_df = pd.DataFrame(
            {
                CASE_NUMBER_COL: df[CASE_NUMBER_COL],
                ALLOCATED_AMOUNT_COL: df[ALLOCATED_AMOUNT_COL],
                ALLOCATION_DATE_COL: df[ALLOCATION_DATE_COL],
                PAYMENT_FOR_COL: df[PAYMENT_FOR_COL],
                RECEIVER_COL: df[RECEIVER_COL],
            }
        )

        frames.append(cleaned_df)
    df = pd.concat(frames, ignore_index=True)
    df = attach_case_ids(df)
    return df

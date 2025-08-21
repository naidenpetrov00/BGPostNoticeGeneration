from fastapi import Request
import pandas as pd
import os
from typing import List

from enums import Offices

folder_path = "./documents"
caseNumberProp = "Дело №"
documentNumber = "Докуемнт №"
outDate = "Изходиран"
recieverProp = "Получател"
adressProp = "Адрес"
debtorName = "Към длъжник"
sender = "Изпращач"


def readExcelFiles() -> List[pd.DataFrame]:
    result: List[pd.DataFrame] = []
    for file_name in os.listdir(folder_path):
        if file_name.endswith(".ods") or file_name.endswith(".xlsx"):
            file_path = os.path.join(folder_path, file_name)
            print(f"Reading: {file_path}")
            data = pd.DataFrame
            try:
                df = pd.read_excel(file_path)
                result.append(
                    df[
                        [
                            caseNumberProp,
                            recieverProp,
                            adressProp,
                            documentNumber,
                            debtorName,
                            outDate,
                        ]
                    ]
                )
            except Exception as e:
                print(f"Error reading {file_path}")
                print(e)

    return result


def read_temp_file(request: Request, name) -> pd.DataFrame:
    office = getattr(request.state, "office", None)
    if office == Offices.NEDELCHO.value:
        return read_temp_file_841(name)
    elif office == Offices.STRAMSKI.value:
        return read_temp_file_870(name)
    elif office == Offices.ROSEN.value:
        return read_temp_file_910(name)
    else:
        print(f"There is not such office in our system")
        return pd.DataFrame()


def read_temp_file_841(name) -> pd.DataFrame:
    try:
        df = pd.read_excel(name)
        print(df.head())
        return df[
            [
                caseNumberProp,
                recieverProp,
                adressProp,
                documentNumber,
                debtorName,
                outDate,
            ]
        ]
    except Exception as e:
        print(f"Error reading file")
        print(e)
        return pd.DataFrame()


def read_temp_file_870(name) -> pd.DataFrame:
    try:
        df = pd.read_excel(name)
        print(df.head())
        return df[
            [
                caseNumberProp,
                recieverProp,
                adressProp,
                documentNumber,
                debtorName,
                outDate,
            ]
        ]
    except Exception as e:
        print(f"Error reading file")
        print(e)
        return pd.DataFrame()


BP_PATTERN = r"(?i)(?:\u0411|B)\s*(?:\u041F|P)"


def read_temp_file_910(path: str) -> pd.DataFrame:
    # 1) read
    df = pd.read_excel(path, dtype=str)

    # 2) keep only rows where "Бележки" contains "БП"
    notes = df["Бележки"].fillna("").astype(str)
    df = df[notes.str.contains(BP_PATTERN, regex=True, na=False)].copy()

    # 3) rename straight into your props
    df = df.rename(
        columns={
            "No дело": caseNumberProp,
            "Адресат": recieverProp,
            "Адрес": adressProp,  # if the file has no "Адрес", we fill it below
            "Изх.No": documentNumber,
        }
    )

    # 4) debtorName = same as receiver (change if you want another source)
    # df[debtorName] = df[recieverProp]

    # 5) outDate from "Дата" -> dd.mm.yyyy
    df[outDate] = (
        pd.to_datetime(df["Дата"], dayfirst=True, errors="coerce")
        .dt.strftime("%d/%m/%Y")
        .fillna("")
    )

    # 6) if "Адрес" column didn’t exist, ensure your prop exists
    if adressProp not in df.columns:
        df[adressProp] = ""

    # 7) return only needed columns (in order)
    return df[
        [
            caseNumberProp,
            recieverProp,
            adressProp,
            documentNumber,
            #  debtorName,
            outDate,
        ]
    ].fillna("")

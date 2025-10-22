from fastapi import Request
import pandas as pd
import os
from typing import Any, List
from enums import Offices, PairMode
import blankField

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


def read_temp_file(
    request: Request, name, mode: PairMode
) -> tuple[pd.DataFrame, Any | None]:
    office = getattr(request.state, "office", None)
    if office == Offices.NEDELCHO.value:
        return read_temp_file_841(name, mode), office
    elif office == Offices.STRAMSKI.value:
        return read_temp_file_870(name, mode), office
    elif office == Offices.ROSEN.value:
        return read_temp_file_910(name, mode), office
    else:
        print(f"There is not such office in our system")
        return pd.DataFrame(), office


def read_temp_file_841(name, mode: PairMode) -> pd.DataFrame:
    try:
        df = pd.read_excel(name)
        blankField.sender_name = "ЧСИ - Неделчо Митев рег.№ 841 тел.: 0700 20 841"
        blankField.sender_address = "1000 София бул.Княз Александър Дондуков №:11"
        blankField.sender_city = "София"
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


def read_temp_file_870(name, mode: PairMode) -> pd.DataFrame:
    try:
        df = pd.read_excel(name)
        blankField.sender_name = "ЧСИ - Иван Стръмски рег.№ 870 тел.: 042 621087"
        blankField.sender_address = "гр. Стара Загора, бул. Руски № 26, ет.3"
        blankField.sender_city = "Стара Загора"

        df = df[df["Вх./Изх."] != "ВХОДЯЩ"]
        df = df[df["Получено /Изпратено/ чрез"] == "Български пощи"]
        df[caseNumberProp] = (
            df["Дело година"].astype(float).astype(int).astype(str)
            + "87004"
            + df["Дело №"].astype(float).astype(int).astype(str).str.zfill(5)
        )

        df = df.rename(
            columns={
                # "Дело №": caseNumberProp,
                "Изпратено на / Получено от": recieverProp,
                "Изпратено на адрес / Получено от": adressProp,  # if the file has no "Адрес", we fill it below
                "№": documentNumber,
                "Дата": outDate,
            }
        )

        if mode == PairMode.compact:
            df = df.groupby([recieverProp, adressProp], as_index=False).agg(
                {
                    documentNumber: lambda x: ", ".join(x.astype(str)),
                    caseNumberProp: lambda x: ", ".join(x.astype(str)),
                    outDate: "first",
                }
            )
        print(df.head(100))
        return df[
            [
                caseNumberProp,
                recieverProp,
                adressProp,
                documentNumber,
                # debtorName,
                outDate,
            ]
        ]
    except Exception as e:
        print(f"Error reading file")
        print(e)
        return pd.DataFrame()


BP_PATTERN = r"(?i)(?:\u0411|B)\s*(?:\u041F|P)"


def read_temp_file_910(path: str, mode: PairMode) -> pd.DataFrame:
    df = pd.read_excel(path, dtype=str)
    blankField.sender_name = "ЧСИ - Росен Раев рег.№ 910 тел.: 032 397050"
    blankField.sender_address = "гр. Стара Загора, бул. Руски № 26, ет.3"
    blankField.sender_city = "Пловдив"

    notes = df["Бележки"].fillna("").astype(str)
    df = df[notes.str.contains(BP_PATTERN, regex=True, na=False)].copy()

    df = df.rename(
        columns={
            "No дело": caseNumberProp,
            "Адресат": recieverProp,
            "Адрес": adressProp,  # if the file has no "Адрес", we fill it below
            "Изх.No": documentNumber,
        }
    )

    # df[debtorName] = df[recieverProp]

    df[outDate] = (
        pd.to_datetime(df["Дата"], dayfirst=True, errors="coerce")
        .dt.strftime("%d/%m/%Y")
        .fillna("")
    )

    if adressProp not in df.columns:
        df[adressProp] = ""

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

import pandas as pd
import os
from typing import List

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

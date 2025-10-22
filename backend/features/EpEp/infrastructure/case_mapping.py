import pandas as pd
from uuid import UUID

from config import CASE_NUMBER_COL
from config.paths import CASEMAPPINGSPATH


def load_case_mapping() -> pd.DataFrame:
    df = pd.read_csv(
        CASEMAPPINGSPATH, dtype={"case_number": "string", "case_id": "string"}
    )

    df["case_id"] = df["case_id"].str.extract(r"([0-9a-fA-F-]{36})")
    return df


def is_valid_uuid(s: str) -> bool:
    try:
        UUID(str(s))
        return True
    except Exception:
        return False


def upsert_mapping(case_number: str, case_id: str) -> None:
    try:
        df = pd.read_csv(
            CASEMAPPINGSPATH, dtype={"case_number": "string", "case_id": "string"}
        )
    except FileNotFoundError:
        df = pd.DataFrame(columns=["case_number", "case_id"])

    mask = df["case_number"] == case_number
    if mask.any():
        df.loc[mask, "case_id"] = case_id
    else:
        df = pd.concat(
            [df, pd.DataFrame([{"case_number": case_number, "case_id": case_id}])],
            ignore_index=True,
        )

    df.to_csv(CASEMAPPINGSPATH, index=False)


def attach_case_ids(df: pd.DataFrame, case_col: str = CASE_NUMBER_COL) -> pd.DataFrame:
    map_df = load_case_mapping()
    out = df.merge(map_df, how="left", left_on=case_col, right_on="case_number")
    out = out.drop(columns=["case_number"])
    return out

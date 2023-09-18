import csv
import io
import re

import pandas as pd

from fastapi import HTTPException


def read_csv(file_route):
    with open(f"{file_route}", "r") as file:
        csv_reader = csv.reader(file, delimiter="\t")
        header = next(csv_reader)
        date_reg = r"^\d{2}\.\d{2}\.\d{4}$"
        data_to_insert = []
        for row in csv_reader:
            row_dict = {}
            for idx, column in enumerate(header):
                if not row[idx]:
                    row[idx] = None
                elif re.match(date_reg, row[idx]):
                    row[idx] = "-".join(row[idx].split(".")[::-1])
                row_dict[column] = row[idx]
            data_to_insert.append(row_dict)
        return data_to_insert


async def read_xlsx(file):
    data = await file.read()
    df = pd.read_excel(io.BytesIO(data), engine="openpyxl")
    if df.empty:
        raise HTTPException(status_code=400, detail="Error: no data in file")
    missing_columns = [column for column in ("period", "sum", "category_plan") if column not in df.columns]
    if missing_columns:
        missing_columns_str = ", ".join(missing_columns)
        raise HTTPException(
            status_code=400, detail=f"Error: no '{missing_columns_str}' column"
        )
    if not df["period"].notna().all():
        raise HTTPException(
            status_code=400, detail="Error: column 'period' must not be empty"
        )
    if not df["period"].dtype == "datetime64[ns]":
        raise HTTPException(
            status_code=400, detail="Error: column 'period' must be all date type"
        )
    df["period_valid"] = pd.to_datetime(df["period"], errors="coerce")
    df["day_of_month"] = df["period_valid"].dt.day
    if (df["day_of_month"] != 1).any():
        raise HTTPException(status_code=400, detail="Error: day of month must be 1")
    df = df.drop(columns=["period_valid", "day_of_month"])
    valid_categories = ["видача", "збір"]
    if not df["category_plan"].isin(valid_categories).all():
        raise HTTPException(
            status_code=400,
            detail="Error: not all categories are valid, must be 'видача' or 'збір'",
        )
    if df.duplicated(subset=["category_plan", "period"]).any():
        raise HTTPException(
            status_code=400,
            detail="Error: duplicated data of 'category_plan' and 'period'",
        )
    for date in df["period"].unique():
        if (
            "видача" in df[(df["period"] == date)]["category_plan"].values
            and "збір" not in df[(df["period"] == date)]["category_plan"].values
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Error: for date '{date.date()}' must be category 'видача' and 'збір'",
            )
        if (
            "збір" in df[(df["period"] == date)]["category_plan"].values
            and "видача" not in df[(df["period"] == date)]["category_plan"].values
        ):
            raise HTTPException(
                status_code=400,
                detail=f"Error: for date '{date.date()}' must be category 'видача' and 'збір'",
            )
    if not df["sum"].notna().all() or not (df["sum"] >= 0).all():
        raise HTTPException(
            status_code=400, detail="Error: sum must be 0 or greater than 0"
        )
    df["period"] = pd.to_datetime(df["period"], errors="coerce").dt.date.apply(
        lambda x: f"{x}"
    )
    return df.to_dict(orient="records")

from dataclasses import dataclass

import pandas as pd


@dataclass
class HPIDataLoader:
    file_path: str

    def load_data(self) -> pd.DataFrame:
        sheets = pd.read_excel(self.file_path, sheet_name=None)
        dataframes = []

        for sheet_name, df in sheets.items():
            df.columns = df.columns.str.strip().str.lower()
            if "date" in df.columns:
                df["date"] = pd.to_datetime(df["date"], errors="coerce").dt.to_period(
                    "M"
                )
                df = df.rename(
                    columns={
                        col: f"{col}_{sheet_name.lower()}"
                        for col in df.columns
                        if col != "date"
                    }
                )
                dataframes.append(df)

        hpi_data = dataframes[0]
        for df in dataframes[1:]:
            hpi_data = pd.merge(hpi_data, df, on="date", how="outer")

        hpi_data.columns = (
            hpi_data.columns.str.strip().str.lower().str.replace(" ", "_")
        )
        return hpi_data.reset_index(drop=True)

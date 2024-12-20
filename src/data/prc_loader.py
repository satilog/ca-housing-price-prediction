from dataclasses import dataclass

import pandas as pd


@dataclass
class PRCDataLoader:
    file_path: str

    def load_data(self) -> pd.DataFrame:
        prc_data = pd.read_excel(self.file_path)
        prc_data.columns = (
            prc_data.columns.str.strip().str.lower().str.replace(" ", "_")
        )
        prc_data["date"] = pd.to_datetime(
            prc_data["date"], errors="coerce"
        ).dt.to_period("M")
        return prc_data

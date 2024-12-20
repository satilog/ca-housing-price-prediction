from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class DataMerger:
    data_loaders: List

    def merge_data(self) -> pd.DataFrame:
        merged_data = None
        for loader in self.data_loaders:
            data = loader.load_data()
            if merged_data is None:
                merged_data = data
            else:
                merged_data = pd.merge(merged_data, data, on="date", how="inner")
        return merged_data.reset_index(drop=True)

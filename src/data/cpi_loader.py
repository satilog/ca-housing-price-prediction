import pandas as pd
import json
from dataclasses import dataclass

@dataclass
class CPIDataLoader:
    file_path: str

    def load_data(self) -> pd.DataFrame:
        with open(self.file_path, "r") as file:
            cpi_raw_data = json.load(file)
        
        # Extract observations
        observations = cpi_raw_data["observations"]
        flattened_data = []
        for observation in observations:
            row = {"date": observation["d"]}
            for key, value in observation.items():
                if key != "d":  # Skip the date field, already added
                    row[key] = value.get("v", None)  # Get the value field
            flattened_data.append(row)

        # Create DataFrame
        cpi_data = pd.DataFrame(flattened_data)

        # Normalize column names
        cpi_data.columns = cpi_data.columns.str.strip().str.lower().str.replace(" ", "_")
        
        # Convert date to a consistent format
        cpi_data['date'] = pd.to_datetime(cpi_data['date'], errors='coerce').dt.to_period('M')
        return cpi_data

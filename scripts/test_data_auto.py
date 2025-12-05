import pandas as pd
from scripts.data_handler import DataHandler
from pathlib import Path
import importlib

importlib.reload(scripts.data_handler) #reloaded the scripts.data_handler as it was picking up wrong one and throwing error

print("Starting test...")

handler = DataHandler(filepath_list=[])

# excel_path=raw_dir / "IRENA_renewable_energy_data.xlsx"
# xls = pd.ExcelFile(excel_path)
# print(xls.sheet_names)

print("Testing data handler")
handler.excel_to_csv(
    excel_path="data/raw/IRENA_renewable_energy_data.xlsx",
    output_dir="data/raw/",
    sheets=["Pivot", "Country", "Region ", "Global"]
)
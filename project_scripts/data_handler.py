# DataHandler Class - Automation for loading and cleaning

import pandas as pd
from pathlib import Path
import pycountry  # type: ignore

# Import project_root from project_path_setup
from project_scripts import project_path_setup

project_root = project_path_setup.project_root  # lowercase

class DataHandler:
    """
    A simple helper class for:
    - loading multiple CSV files
    - cleaning the data
    - validating the data
    - merging with other datasets
    """
    def __init__(self, filepath_list, country_col='country', year_col='year'):
        """
        Initialize handler
        filepath_list: list of CSV files (relative to project root)
        country_col: name of the country column
        year_col: name of the year column
        """
        self.filepaths = filepath_list
        self.country_col = country_col
        self.year_col = year_col
        self.df = pd.DataFrame()

    def excel_to_csv(self, excel_path, output_dir, sheets=None, prefix=None):
        """
        Convert selected sheets in an Excel file to individual CSV files.
        Paths are relative to project_root
        """
        output_dir = Path(project_root) / output_dir
        output_dir.mkdir(parents=True, exist_ok=True)

        if prefix is None:
            prefix = Path(excel_path).stem.lower()

        xls = pd.ExcelFile(Path(project_root) / excel_path)

        if sheets is None:
            sheets = xls.sheet_names

        for sheet in sheets:
            try:
                df = pd.read_excel(xls, sheet_name=sheet)
                csv_name = output_dir / f"{prefix}_{sheet.lower().replace(' ', '_')}.csv"
                df.to_csv(csv_name, index=False)
                print(f"Saved {csv_name}")
            except Exception as e:
                print(f"Could not read sheet '{sheet}' — {e}")

    def load_file(self, file):
        #file = Path(project_root) / file
        file = Path(file)
        if not file.exists():
            print(f"File not found: {file}")
            return None
        
        if file.suffix == ".csv":
            try:
                return pd.read_csv(file)
            except UnicodeDecodeError:
                print(f"Retrying {file.name} with latin1/utf-8-sig...")
                return pd.read_csv(file, encoding="utf-8-sig", engine="python", on_bad_lines="skip")
        elif file.suffix in [".xlsx", ".xls"]:
            return pd.read_excel(file)
        else:
            print(f"Unsupported file format: {file}")
            return None

    def load_and_combine(self):
        temp_dfs = []
        for file in self.filepaths:
            print(f"Loading: {file}")
            df_temp = self.load_file(file)
            if df_temp is not None:
                temp_dfs.append(df_temp)
            else:
                print(f"Skipped file: {file}")
        self.df = pd.concat(temp_dfs, ignore_index=True)
        print(f"\nLoaded {len(temp_dfs)} files — combined shape: {self.df.shape}")
        return self.df

    def clean_data(self):
        """
        Standardize column names, remove duplicates, convert country names to ISO3
        """
        self.df.columns = (self.df.columns.str.strip()
                           .str.lower()
                           .str.replace(" ", "_"))

        if self.year_col in self.df.columns:
            self.df[self.year_col] = pd.to_numeric(self.df[self.year_col], errors="coerce")

        def country_to_iso(name):
            try:
                return pycountry.countries.lookup(name).alpha_3
            except:
                return None

        if self.country_col in self.df.columns:
            self.df['country_iso'] = self.df[self.country_col].apply(country_to_iso)

        self.df = self.df.drop_duplicates()
        print(f"Data cleaned: shape {self.df.shape}")
        return self.df


def load_csv(relative_path: str):
    """Load a CSV file given a path relative to project root"""
    return pd.read_csv(Path(project_root) / relative_path)

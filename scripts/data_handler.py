# DataHandler Class -Automation for loading and cleaning
# Imports
import pandas as pd
import pycountry
from pathlib import Path

class DataHandler:
    """
    A simple helper class for:
    - loading multiple CSV files
    - cleaning the data
    - validating the data
    - merging with other datasets
    """
    #runs automatically when a new DataHandler is created
    def __init__(self, filepath_list, country_col='country', year_col='year'):
        """
        Initialize handler
        filepath_list: list of CSV files
        country_col: name of the country column
        year_col: name of the year column
        """
        self.filepaths = filepath_list
        self.country_col = country_col
        self.year_col = year_col
        self.df = pd.DataFrame()
        
    # 1. Convert Excel to CSV (One-Time Preprocessing)
    def excel_to_csv(self, excel_path, output_dir, sheets=None, prefix=None):
        """
        Convert selected sheets in an Excel file to individual CSV files.
        
        excel_path : path to the .xlsx file
        output_dir : folder where CSVs will be saved
        sheets     : list of sheet names to extract (None = all sheets)
        prefix     : optional string to prefix CSV filenames (default: excel filename)
        """
        print(f"Called excel_to_csv with {excel_path=}, {output_dir=}, {sheets=}, {prefix=}")
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        if prefix is None:
        # Default: use the Excel filename (without extension) as prefix
            prefix = Path(excel_path).stem.lower()
        
        xls = pd.ExcelFile(excel_path)

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

    # 2. File loader (CSV , Excel , encoding fix)
    def load_file(self, file):
        file = Path(file)
        # CSV handling
        if file.suffix == ".csv":
            try:
                return pd.read_csv(file)
            except UnicodeDecodeError:
                print(f"Retrying {file.name} with latin1/utf-8-sig...")
                return pd.read_csv(
                    file,
                    encoding="utf-8-sig",
                    engine="python",
                    on_bad_lines="skip"
                )

        # Excel fallback
        elif file.suffix in [".xlsx", ".xls"]:
            return pd.read_excel(file)
        else:
            print(f"Unsupported file format: {file}")
            return None
    
    # Load combined data
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
        print(f"\n Loaded {len(temp_dfs)} files — combined shape: {self.df.shape}")
        return self.df
    
    
    # def load_and_combine(self):
    #     """
    #     Load multiple CSV files and combine into a single dataframe
    #     """
    #     temp_dfs = []
    #     for file in self.filepaths:
    #         temp = pd.read_csv(file)
    #         temp_dfs.append(temp)
    #     self.df = pd.concat(temp_dfs, ignore_index=True)
    #     print(f"Loaded {len(self.filepaths)} files, combined shape: {self.df.shape}")
    #     return self.df
    

    def clean_data(self):
        """
        Standardize column names, remove duplicates, convert country names to ISO3
        """
        # Standardize column names, Remove spaces before/after names,Convert names to lowercase.
        self.df.columns = (self.df.columns.str.strip()
            .str.lower()
            .str.replace(" ", "_")
        )
        
         # convert year
        if self.year_col in self.df.columns:
            self.df[self.year_col] = pd.to_numeric(self.df[self.year_col], errors="coerce")


        # function to convert country name to ISO code
        # converting name to a 3-letter ISO code, If it fails (name not found) it returns None
        def country_to_iso(name):
            try:
                return pycountry.countries.lookup(name).alpha_3
            except:
                return None
            
        # add new column for ISO codes    
        if self.country_col in self.df.columns:
            self.df['country_iso'] = self.df[self.country_col].apply(country_to_iso)
        
        # Drop duplicates
        self.df = self.df.drop_duplicates()
        
        # handle missing values 
        # self.df = self.df.dropna()
        
        print(f"Data cleaned: shape {self.df.shape}")
        return self.df
    
    
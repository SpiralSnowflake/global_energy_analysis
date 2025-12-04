# DataHandler Class -Automation for loading and cleaning
# Imports
import pandas as pd
import pycountry

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
    
    def load_and_combine(self):
        """
        Load multiple CSV files and combine into a single dataframe
        """
        temp_dfs = []
        for file in self.filepaths:
            temp = pd.read_csv(file)
            temp_dfs.append(temp)
        self.df = pd.concat(temp_dfs, ignore_index=True)
        print(f"Loaded {len(self.filepaths)} files, combined shape: {self.df.shape}")
        return self.df

    def clean_data(self):
        """
        Standardize column names, handle missing values, remove duplicates, convert country names to ISO3
        """
        # Standardize column names, Remove spaces before/after names,Convert names to lowercase.
        self.df.columns = self.df.columns.str.strip().str.lower()

        # function to convert country name to ISO code
        # converting name to a 3-letter ISO code, If it fails (name not found) it returns None
        def country_to_iso(name):
            try:
                return pycountry.countries.lookup(name).alpha_3
            except:
                return None
            
        # add new column for ISO codes    
        self.df['country_iso'] = self.df[self.country_col].apply(country_to_iso)
        
        # Convert year column to numeric, Turns year values into integers,If something is not a number it becomes NaN.
        self.df[self.year_col] = pd.to_numeric(self.df[self.year_col], errors='coerce')
        
        # Drop duplicates
        self.df = self.df.drop_duplicates()
        
        # Optionally handle missing values here (e.g., drop or fillna)
        # self.df = self.df.dropna()
        
        print(f"Data cleaned: shape {self.df.shape}")
        return self.df
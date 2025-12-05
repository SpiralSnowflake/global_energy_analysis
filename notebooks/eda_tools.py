# Imports
import pandas as pd
import numpy as np
from IPython.display import display
import matplotlib.pyplot as plt
import seaborn as sns

# EDA Feature/Structure
# 1.Quick overview: first_glance, summary_stats
# 2.Missing data check: missing_report
# 3.Duplicates: check_duplicates
# 4.Column type detection: get_column_types
# 5.Univariate plots: plot_distribution, plot_boxplot
# 6.Categorical counts: value_counts
# 7.Bivariate analysis: plot_scatter, correlation_matrix

class EDA_Analyzer:
    def __init__(self, df):
        """
        Initialize with a pandas DataFrame
        """
        self.df = df.copy()
   
    # 1. Basic Info
    def first_glance(self, n=5):
        print("----- First few rows -----")
        display(self.df.head(n))
        print("\n----- Data Shape -----")
        print(self.df.shape)
        print("\n----- Column Types -----")
        print(self.df.dtypes)
    
    def summary_stats(self):
        print("----- Summary Statistics -----")
        display(self.df.describe(include='all').T)
    
    # 2. Missing Data
    def missing_report(self):
        print("----- Missing Values -----")
        missing = self.df.isna().sum()
        missing_percent = (missing / len(self.df)) * 100
        report = pd.DataFrame({'Missing Count': missing, 'Missing %': missing_percent})
        display(report.sort_values(by='Missing %', ascending=False))
    
    # 3. Duplicate Records
    def check_duplicates(self):
        total_duplicates = self.df.duplicated().sum()
        print(f"Total duplicate rows: {total_duplicates}")
    
    # 4. Column Types
    def get_column_types(self):
        numeric_cols = self.df.select_dtypes(include=[np.number]).columns.tolist()
        categorical_cols = self.df.select_dtypes(include=['object', 'category']).columns.tolist()
        print(f"Numeric columns ({len(numeric_cols)}): {numeric_cols}")
        print(f"Categorical columns ({len(categorical_cols)}): {categorical_cols}")
        return numeric_cols, categorical_cols
    
    # 5. Univariate Analysis
    def plot_distribution(self, col, bins=30):
        plt.figure(figsize=(8,4))
        sns.histplot(self.df[col].dropna(), bins=bins, kde=True)
        plt.title(f'Distribution of {col}')
        plt.show()
    
    def plot_boxplot(self, col):
        plt.figure(figsize=(6,4))
        sns.boxplot(x=self.df[col])
        plt.title(f'Boxplot of {col}')
        plt.show()
    
    def value_counts(self, col):
        print(f"Value counts for {col}:")
        display(self.df[col].value_counts())
    
    # 6. Bivariate Analysis
    def plot_scatter(self, col1, col2):
        plt.figure(figsize=(6,4))
        sns.scatterplot(x=self.df[col1], y=self.df[col2])
        plt.title(f'{col1} vs {col2}')
        plt.show()
    
    def correlation_matrix(self):
        numeric_cols, _ = self.get_column_types()
        corr = self.df[numeric_cols].corr()
        plt.figure(figsize=(10,8))
        sns.heatmap(corr, annot=True, fmt=".2f", cmap='coolwarm')
        plt.title('Correlation Matrix')
        plt.show()
        return corr
    
    # 7. Time-Series (if column 'year' exists)
    def plot_time_series(self, col, country=None):
        if 'year' not in self.df.columns:
            print("No 'year' column for time-series plot.")
            return
        df_plot = self.df.copy()
        if country:
            df_plot = df_plot[df_plot['country'] == country]
        plt.figure(figsize=(10,4))
        sns.lineplot(x='year', y=col, data=df_plot)
        title = f"{col} over time"
        if country:
            title += f" ({country})"
        plt.title(title)
        plt.show()
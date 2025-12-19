#It provides helper functions to connect to the database, run SQL queries, 
# manage image folders, and save Plotly charts as HTML/PNG.
"""
Utility functions for:
- Database connection and queries
- Image and output folder management
- Saving Plotly charts
"""

import os
import sqlite3
import pandas as pd
import plotly.io as pio
import plotly.express as px

# Import project root from project_path_setup
from project_scripts.project_path_setup import project_root

# Force Kaleido for static images
pio.kaleido.scope.default_format = "png"
pio.kaleido.scope.default_width = 1200
pio.kaleido.scope.default_height = 800
pio.kaleido.scope.default_scale = 2

# ---------------------------
# Paths (relative to project_root)
# ---------------------------
DB_PATH = project_root / "db" / "renewable_energy.db"
IMAGES_PATH = project_root / "images"
DATA_PATH = project_root / "data" / "final"
OUTPUT_PATH = project_root / "output"

# Ensure folders exist
os.makedirs(IMAGES_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---------------------------
# Functions
# ---------------------------
def get_image_folder(subfolder: str):
    """Return full path for a subfolder in images folder and create it if missing."""
    path = IMAGES_PATH / subfolder
    os.makedirs(path, exist_ok=True)
    return path

def connect_db():
    """Return a sqlite3 connection to the project database."""
    return sqlite3.connect(DB_PATH)

def run_sql(query: str):
    """Run SQL query and return a pandas DataFrame."""
    with connect_db() as conn:
        df = pd.read_sql(query, conn)
    return df

def save_plot(fig, folder: str, filename: str):
    """
    Save Plotly figure as HTML (always) and PNG (if possible)
    """
    folder_path = get_image_folder(folder)
    html_path = folder_path / f"{filename}.html"
    png_path = folder_path / f"{filename}.png"
    
    # Save HTML
    fig.write_html(html_path)
    
    # Save PNG
    try:
        fig.write_image(png_path)
    except Exception as e:
        print("PNG export skipped — reason:", e)
        print("→ HTML file still works.")

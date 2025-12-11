#It provides helper functions to connect to the database, run SQL queries, 
# manage image folders, and save Plotly charts as HTML/PNG.
import os
from dotenv import load_dotenv
import sqlite3
import plotly.express as px
import pandas as pd

# Load .env variables
load_dotenv()

import plotly.io as pio

# Force Kaleido as engine for static images
pio.kaleido.scope.default_format = "png"  # PNG format
pio.kaleido.scope.default_width = 1200    # optional: image width
pio.kaleido.scope.default_height = 800    # optional: image height
pio.kaleido.scope.default_scale = 2       # optional: scale for retina quality


# ---------------------------
# Paths
# ---------------------------
PROJECT_ROOT = os.getenv("PROJECT_ROOT", os.getcwd())
DB_PATH = os.path.join(PROJECT_ROOT, os.getenv("DB_PATH", "db/renewable_energy.db"))
IMAGES_PATH = os.path.join(PROJECT_ROOT, os.getenv("IMAGES_PATH", "images"))
DATA_PATH = os.path.join(PROJECT_ROOT, os.getenv("DATA_PATH", "data/final"))
OUTPUT_PATH = os.path.join(PROJECT_ROOT, os.getenv("OUTPUT_PATH", "output"))

# Ensure images/output folders exist
os.makedirs(IMAGES_PATH, exist_ok=True)
os.makedirs(OUTPUT_PATH, exist_ok=True)

# ---------------------------
# Functions
# ---------------------------

def get_image_folder(subfolder: str):
    """
    Returns full path for a subfolder in images folder.
    Creates folder if it doesn't exist.
    """
    path = os.path.join(IMAGES_PATH, subfolder)
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
    html_path = os.path.join(folder_path, f"{filename}.html")
    png_path = os.path.join(folder_path, f"{filename}.png")
    
    # Save HTML (interactive)
    fig.write_html(html_path)
    #print("HTML saved:", html_path)
    
    # Save PNG (try)
    try:
        fig.write_image(png_path, engine="kaleido")
        #print("PNG saved:", png_path)
    except Exception as e:
        print("PNG export skipped — reason:", e)
        print("→ HTML file still works.")

"""
create_db.py

Reads the SQL schema to create tables in SQLite,
then loads CSV files into their respective tables to build the project database.
"""

import sqlite3
import pandas as pd
from pathlib import Path

import project_path_setup

project_root = project_path_setup.project_root

db_path = project_root / "db" / "renewable_energy.db"
csv_dir = project_root / "data" / "sqlite"
schema_file = project_root / "db" / "create_schema.sql"

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

with open(schema_file, "r") as f:
    schema_sql = f.read()
conn.executescript(schema_sql)
print("Tables created successfully.")

tables = {
    "country": "country.csv",
    "irena_energy": "irena_energy.csv",
    "owid_co2": "owid_co2.csv",
    "wgi_governance": "wgi_governance.csv",
    "derived_metrics": "derived_metrics.csv"
}

for table, file in tables.items():
    csv_path = csv_dir / file
    if not csv_path.exists():
        print(f"Warning: {file} not found in {csv_dir}")
        continue
    df = pd.read_csv(csv_path)
    df.to_sql(table, conn, if_exists='append', index=False)
    print(f"{table} loaded successfully.")

conn.commit()
conn.close()
print("Database creation and CSV loading complete!")

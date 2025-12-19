"""
data_sql_csvs.py

Loads the merged dataset, cleans column names, and splits it into multiple CSV files for analysis:
- country information
- IRENA energy data
- CO₂ emissions
- governance indicators
- derived metrics
"""

import pandas as pd
from pathlib import Path

import project_path_setup

# Project root
project_root = project_path_setup.project_root

# Paths
input_csv = project_root / "data" / "final" / "final_combined.csv"
output_dir = project_root / "data" / "sqlite"
output_dir.mkdir(parents=True, exist_ok=True)

# Load merged dataset
df = pd.read_csv(input_csv, low_memory=False)

# Clean column names
def clean_column_names(col):
    col = col.lower().replace(" ", "_").replace("-", "_")
    col = col.replace("/", "_")
    col = col.replace("(", "").replace(")", "").replace(".", "_").replace("*", "")
    return col.strip()

df.columns = [clean_column_names(c) for c in df.columns]

# ---- 1. Country CSV ----
dim_country_cols = ["iso", "country", "region", "sub_region"]
dim_country = df[dim_country_cols].drop_duplicates(subset=["iso"])
dim_country.to_csv(output_dir / "country.csv", index=False)

# ---- 2. IRENA energy CSV (AGGREGATED, NOT DEDUPED) ----

fact_irena_cols = [
    "iso", "year",
    "sdg_7b1_re_capacity_per_capita_w_inhabitant",
    "electricity_generation_gwh",
    "electricity_installed_capacity_mw",
    "heat_generation_tj",
    "public_flows_2022_usd_m",
    "sdg_7a1_intl__public_flows_2022_usd_m",
    "group_technology",
    "technology",
    "re_or_non_re"
]

# 1. Select required columns
fact_irena = df[fact_irena_cols].copy()

# 2. Rename to DB-friendly column names
fact_irena = fact_irena.rename(columns={
    "sdg_7b1_re_capacity_per_capita_w_inhabitant": "sdg_7b1_capacity_per_capita",
    "sdg_7a1_intl__public_flows_2022_usd_m": "sdg_7a1_flows",
    "public_flows_2022_usd_m": "public_flows"
})

# 3. Aggregate to enforce correct grain:
#    iso × year × group_technology × technology × re_or_non_re
fact_irena = (
    fact_irena
    .groupby(
        ["iso", "year", "group_technology", "technology", "re_or_non_re"],
        dropna=False,
        as_index=False
    )
    .agg({
        "sdg_7b1_capacity_per_capita": "mean",   # per-capita metric
        "electricity_generation_gwh": "sum",
        "electricity_installed_capacity_mw": "sum",
        "heat_generation_tj": "sum",
        "public_flows": "sum",
        "sdg_7a1_flows": "sum"
    })
)

# 4. Save aggregated IRENA energy table
fact_irena.to_csv(output_dir / "irena_energy.csv", index=False)


# ---- 3. OWID CO2 CSV ----
fact_owid_cols = [
    "iso", "year","co2", "co2_per_capita", "co2_per_gdp",
    "coal_co2", "oil_co2", "gas_co2", "methane", "nitrous_oxide", "total_ghg",
    "co2_growth_prct","energy_per_capita"
]
fact_owid = df[fact_owid_cols].drop_duplicates(subset=["iso", "year"])
fact_owid.to_csv(output_dir / "owid_co2.csv", index=False)

# ---- 4. WGI governance CSV ----
wgi_cols = ["iso", "year", "indicator", "estimate"]
fact_wgi = df[wgi_cols].dropna(subset=["estimate"]).drop_duplicates(subset=["iso", "year", "indicator"])
fact_wgi.to_csv(output_dir / "wgi_governance.csv", index=False)

# ---- 5. Derived Metrics CSV ----
derived_cols = [
    "iso", "year", "co2_per_capita", "sdg_7b1_re_capacity_per_capita_w_inhabitant",
    "trade_co2_share", "cumulative_other_co2"
]
derived_metrics = df[derived_cols].drop_duplicates(subset=["iso", "year"])
derived_metrics = derived_metrics.rename(columns={
    "sdg_7b1_re_capacity_per_capita_w_inhabitant": "sdg_7b1_capacity_per_capita"
})
derived_metrics.to_csv(output_dir / "derived_metrics.csv", index=False)

print("All 5 CSVs created successfully in:", output_dir)

# Exploring Global Renewable Energy Trends and Drivers

## Project Overview
This project explores global renewable energy trends and drivers using multiple datasets. The goal is to integrate environmental, economic, and governance indicators to understand renewable energy adoption and its impact on CO₂ emissions and energy patterns globally.

---

## Interactive Plot: Global Renewable Generation Over Time

Explore how renewable energy generation evolves globally over time using the interactive Plotly chart below:

<iframe src="images/rq7/renewable_elec_trend.html" width="100%" height="600" style="border:none;"></iframe>

You can explore the interactive global renewable generation over time plot here:  
[Interactive Plot HTML](images/rq7/renewable_elec_trend.html)

[![Interactive Plot Preview](images/rq7/renewable_elec_trend_preview.png)]



---

## Datasets

| Dataset | Source | Description |
|---------|--------|-------------|
| OWID CO₂ | [Our World in Data](https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions) | Country-level CO₂ emissions, energy use, and population data. |
| IRENA Renewable Energy | [IRENA Excel](https://www.irena.org/Statistics) | Renewable energy capacity, generation, and financing data (Pivot, Country, Region, Global sheets). |
| WGI Governance Indicators | [World Bank WGI](https://info.worldbank.org/governance/wgi/) | Worldwide governance indicators by country and year. |

---

## Project Steps

| Step | Description |
|------|-------------|
| 1. Data Loading & Automation | Use DataHandler class to convert Excel sheets to CSV, load datasets, standardize column names, and handle duplicates. |
| 2. Data Cleaning & Missing Values | Standardize ISO codes, handle missing values (median imputation for energy, linear interpolation for GDP/population), separate countries vs regions. |
| 3. Exploratory Data Analysis (EDA) | Examine data types, missing values, trends, outliers, and descriptive statistics per dataset. |
| 4. Data Merging | Merge IRENA + OWID → merged result + WGI. Retain all IRENA rows; missing OWID/WGI data as NaN. |
| 5. Data Normalization | Convert numeric columns stored as objects to numeric, categorical columns to category, and year to datetime. |
| 6. Imputation & Derived Metrics | Fill missing energy data per country using median; interpolate population/GDP; calculate per-capita and derived metrics. |
| 7. Final Dataset Validation | Check descriptive statistics, missing values, distributions, and skewness. Save final combined dataset. |
| 8. Database Preparation | Design normalized ERD, build SQLite database, define tables with primary keys and foreign keys. |
| 9. SQL Queries & Aggregations | Create queries for country-level, regional, and global trends. |
| 10. Visualizations & Dashboard | Create interactive plots, time series, heatmaps, and global trend visualizations. |

---

## Key Analysis Questions
| How are global renewable energy trends evolving over time? This explores the changes in renewable capacity and generation by country/region . Trends in CO₂ emissions per capita relative to renewables 
| What are the socio-economic and governance drivers of renewable adoption? This explores the Relationship between GDP, population, governance and renewable energy Key governance indicators associated with adoption 
| How do energy generation patterns vary geographically? Top countries by renewable type.  Heat/electricity generation vs CO₂ per capita 

---

## WGI Indicators Used

| Indicator | Description | Role in Analysis |
|-----------|------------|----------------|
| Voice & Accountability | Citizens’ ability to participate in governance | Assess governance openness effect on renewable adoption |
| Political Stability | Likelihood of political instability or violence | Measures governance stability influence on energy policy |
| Government Effectiveness | Quality of public services and policy | Evaluates effective governance impact on energy programs |
| Regulatory Quality | Ability to implement sound policies | Indicates supportive environment for renewable projects |
| Rule of Law | Enforcement of laws and contracts | Reflects legal environment for energy projects |
| Control of Corruption | Measures corruption | Understanding financing and execution challenges |

---
```
## Directory Structure

project-root/
│
├─ data/
│ ├─ raw/ # Raw Excel/CSV datasets
│ ├─ clean/ # Cleaned CSV datasets
| ├─ final/ # Final merged dataset
│ └─ sqlite/ # csv files for the tables
|
├─ db/
│ ├─ create_schema.sql # database schema script
│ └─ renewable_energy.db
│
├─ project_scripts/
│ ├─ data_handler.py # helper class module for automated data loading and cleaning
| ├─ utils.py # helper module for database and plotting helper functions
| ├─ csv_files_for_tables.py # data preparation and export script 
| ├─ project_path_setup.py #Manages project paths to enable easy relative path access
| └─ create_db.py #load CSVs into DB
│
├─ notebooks/
│ ├─ 01_file_data_ingestion_and_cleaning.ipynb
| ├─ 02_data_wrangling_and_eda.ipynb
│ └─ 03_analysis_and_visualizations.ipynb
│
├─ images/ # Plots
├─ docs/ #Docmentation , including ERD.pdf
├─ README.md
└─ requirements.txt
```
---

## Visual Insights

- **Top Countries by Renewable Generation** – Leading countries and regional patterns.  
- **Renewable Generation Over Time** – Tracks global adoption trends and growth by technology.  
- **CO₂ Emissions vs Renewable Adoption** – Compares per-capita emissions with renewable deployment.  
- **Governance Influence** – Explores links between governance indicators and renewable adoption.

---

## Database & ERD

- ERD diagram located at: `docs/ERD.pdf`  
- SQLite database: `db/renewable_energy.db`  
- Tables are linked using ISO codes, year, and primary/foreign keys for analysis.

---


## Getting Started

To replicate this project on your machine, follow these steps:

### 1. Clone the repository
```bash
git clone https://github.com/SpiralSnowflake/global_energy_analysis.git
cd global_energy_analysis
````

### 2. Create and activate a virtual environment

**Windows:**

```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Linux / MacOS:**

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Notebooks and Database setup

Open and run the notebooks/scripts in order for a smooth workflow:

1. `01_file_data_inspect_cleanup.ipynb`
2. `02_data_wrangling_eda.ipynb`
3. Run the `csv_files_for_tables.py` and `create_db.py` script to load the CSV datasets into the SQLite database:

```bash
python project_scripts/csv_files_for_tables.py
python project_scripts/create_db.py
```

This will generate `renewable_energy.db` in the `db/` folder.

4. For Analysis and Visualizations use `03_analysis_visualizations.ipynb` notebook

### 4. Deactivate environment (after finishing)

```bash
deactivate
```

## Acknowledgments

- Data sources: [IRENA](https://www.irena.org/Statistics), [Our World in Data](https://ourworldindata.org/co2-and-other-greenhouse-gas-emissions), [World Bank WGI](https://info.worldbank.org/governance/wgi/)  
- Project inspired by interest in climate and renewable energy solutions.  
- AI assistance was used for debugging, formatting, and README drafting.  



![Renewable Energy Trends](docs/ren_energy_image.jpg)

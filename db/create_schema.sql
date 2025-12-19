-- Drop tables if they exist
DROP TABLE IF EXISTS country;
DROP TABLE IF EXISTS irena_energy;
DROP TABLE IF EXISTS owid_co2;
DROP TABLE IF EXISTS wgi_governance;
DROP TABLE IF EXISTS derived_metrics;

-- Country table
CREATE TABLE country (
    iso TEXT PRIMARY KEY,
    country TEXT,
    region TEXT,
    sub_region TEXT
);

-- IRENA energy
CREATE TABLE irena_energy (
    iso TEXT,
    year INTEGER,
    group_technology TEXT,
    technology TEXT,
    re_or_non_re TEXT,
    sdg_7b1_capacity_per_capita REAL,
    electricity_generation_gwh REAL,
    electricity_installed_capacity_mw REAL,
    heat_generation_tj REAL,
    public_flows REAL,
    sdg_7a1_flows REAL,
    PRIMARY KEY (iso, year, group_technology, technology, re_or_non_re),
    FOREIGN KEY (iso) REFERENCES country(iso)
);

-- OWID CO2
CREATE TABLE owid_co2 (
    iso TEXT,
    year INTEGER,
    co2 REAL,
    co2_per_capita REAL,
    co2_per_gdp REAL,
    coal_co2 REAL,
    oil_co2 REAL,
    gas_co2 REAL,
    methane REAL,
    nitrous_oxide REAL,
    total_ghg REAL,
    co2_growth_prct REAL,
    energy_per_capita REAL,
    PRIMARY KEY (iso, year),
    FOREIGN KEY (iso) REFERENCES country(iso)
);

-- WGI Governance
CREATE TABLE wgi_governance (
    iso TEXT,
    year INTEGER,
    indicator TEXT,
    estimate REAL,
    PRIMARY KEY (iso, year, indicator),
    FOREIGN KEY (iso) REFERENCES country(iso)
);


-- Derived Metrics
CREATE TABLE derived_metrics (
    iso TEXT,
    year INTEGER,
    co2_per_capita REAL,
    sdg_7b1_capacity_per_capita REAL,
    trade_co2_share REAL,
    cumulative_other_co2 REAL,
    PRIMARY KEY (iso, year),
    FOREIGN KEY (iso) REFERENCES country(iso)
);


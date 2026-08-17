# Methodology

## 1. Objective

The objective of this project was to analyse Great Britain's electricity demand and generation patterns between 2020 and 2025 using half-hourly data.

The analysis focused on:

- Electricity demand
- Peak demand
- Generation mix
- Renewable generation
- Wind generation
- Gas generation
- Residual/net demand
- Daily and seasonal demand patterns

The analysis was designed to answer practical questions relevant to energy-system analysis and trading.

---

# 2. Data Sources

The project uses Great Britain electricity system data covering 2020–2025.

The datasets contain half-hourly observations of electricity demand and generation by fuel type.

The generation dataset contains sources including:

- Gas
- Wind
- Nuclear
- Biomass
- Hydro
- Coal
- Oil
- Pumped storage
- Other generation

Demand data was combined with generation data using the appropriate time and settlement-period fields.

---

# 3. Data Structure

The final analytical dataset contains one observation per half-hourly settlement period.

Key fields include:

| Field | Description |
|---|---|
| `datetime_uk` | UK settlement datetime |
| `settlementDate` | Settlement date |
| `settlementPeriod` | Half-hour settlement period |
| `demand_mw` | Electricity demand in MW |
| `gas_mw` | Gas generation in MW |
| `wind_mw` | Wind generation in MW |
| `renewable_generation_mw` | Total renewable generation in MW |
| `net_demand_mw` | Demand remaining after renewable generation |
| `year` | Calendar year |
| `hour` | Hour of day |
| `day_of_week` | Day of week |
| `season` | Season classification |

---

# 4. Data Preparation

## 4.1 Data inspection

The raw datasets were initially inspected for:

- Number of rows
- Number of columns
- Data types
- Missing values
- Duplicate timestamps
- Date coverage
- Settlement-period consistency
- Quality flags

This ensured that problems in the raw data could be identified before analysis.

---

## 4.2 Timestamp construction

The original data contained settlement dates and settlement periods.

A UK datetime field was constructed to represent the start time of each half-hour settlement period.

The settlement period was converted into a time offset so that:

- Settlement Period 1 represents 00:00
- Settlement Period 2 represents 00:30
- Settlement Period 3 represents 01:00

and so on.

The resulting timestamp was stored as:
```text
datetime_uk

Additional checks were performed to verify that the constructed timestamps aligned correctly with the source data.

5. Data Quality Checks

Several validation checks were performed throughout the preparation process.
Duplicate checks
The datasets were checked for duplicate timestamps and duplicate settlement periods.
Missing values
Important analytical columns were checked for missing observations.
Date coverage

The final datasets were checked to confirm coverage across:
2020–2025
Settlement periods
Each day was expected to contain the appropriate number of half-hour settlement periods, with leap years accounting for additional days.
Dataset alignment
Demand and generation datasets were aligned using their common time dimensions before being merged.

6. Generation Aggregation

Generation data was originally recorded by fuel type.

Fuel-specific generation fields were retained, including:

- Gas
- Wind
- Nuclear
- Biomass
- Hydro
- Coal
- Oil
- Pumped storage
- Other generation

Renewable generation was aggregated from the relevant renewable fuel categories.

The resulting metric was stored as:
renewable_generation_mw

7. Feature Engineering

Additional variables were created to support the analysis.

7.1 Time features

The following fields were derived:

- year
- month
- month_name
- hour
- minute
- day_of_week
- day_of_week_num
- season
- is_weekend

These enabled analysis of hourly, weekly, seasonal and yearly patterns.

7.2 Renewable share

Renewable contribution was calculated relative to electricity demand.

The analytical definition used in the project is:
Renewable Share =
Average Renewable Generation / Average Electricity Demand

This metric was used to evaluate how the contribution of renewable generation changed over time.

7.3 Net demand

Net demand was calculated as:
Net Demand =
Electricity Demand - Renewable Generation

This represents the portion of electricity demand remaining after renewable generation is accounted for.

Net demand was used as an operational indicator of the residual requirement that must be met by other generation sources, imports or system flexibility.

7.4 Gas share

Gas generation was compared with total electricity demand to create a gas contribution metric.
This was used to assess changes in the role of gas generation over time.

7.5 Demand bands

Demand observations were classified into demand bands to support analysis of:
- Low demand
- Normal demand
- High demand
- Peak demand

The bands were used in Power BI to support filtering and segmentation.

7.6 Peak demand indicators

Two peak indicators were created:
is_peak_global
is_peak_year

These distinguish the overall maximum demand observation from the maximum demand observed within each year.

8. Exploratory Analysis

Python was used to analyse the resulting dataset.

The analysis examined:
Annual trends
Average demand
Peak demand
Average gas generation
Average renewable generation
Average wind generation
Average net demand
Hourly patterns
Average demand by hour
Average net demand by hour
Renewable generation by hour
Weekly patterns
Average demand by day of week
Generation mix
Gas
Wind
Nuclear
Hydro
Biomass
Coal
Other generation

9. Key Analytical Calculations
The final analysis compared annual values between 2020 and 2025.

For example:
Percentage Change =
(2025 Value - 2020 Value) / 2020 Value × 100

This was used to quantify changes in:

Demand
Renewable generation
Wind generation
Net demand

Gas generation was also assessed relative to its 2022 maximum average level.

10. Power BI Dashboard

The processed dataset was imported into Power BI.
A dedicated date table was created to support time-based analysis.

The dashboard was divided into four pages:
Executive Overview
High-level system indicators and generation trends.
Demand & Peak Analysis
Demand levels, peak demand and time-of-day patterns.
Generation & Renewable Analysis
Renewable generation, renewable share and generation mix.
Operational Patterns
Net demand and renewable availability across time.

11. Analytical Interpretation
The analysis is primarily descriptive
Observed relationships are not automatically interpreted as causal relationships.

For example, the project identifies that:
Renewable generation increased
Gas generation declined after 2022
Net demand declined

However, the analysis does not establish that renewable growth alone caused the decline in gas generation.

Other factors could contribute, including:
Fuel prices
Weather
Generator availability
Electricity prices
Interconnector flows
Policy changes
System conditions

These factors are outside the current project scope.

12. Reproducibility

The project is structured so that the analysis can be reproduced using the files contained in the repository.

uk_energy_analysis/
│
├── data/
│   ├── raw/
│   └── processed/
│
├── notebooks/
│
├── scripts/
│
├── outputs/
│
├── dashboard/
│
├── docs/
│
├── requirements.txt
└── README.md

Python dependencies are defined in:
requirements.txt 
A fresh Python virtual environment can therefore be created and populated using the project requirements.

13. Limitations

The analysis does not currently include:
Electricity prices
Weather variables
Fuel prices
Carbon prices
Generator outage information
Interconnector flows
Imports and exports
Balancing-market data

These variables could provide additional context for understanding generation decisions and market behaviour.

14. Future Analysis

Potential extensions include:
Linking demand and generation to electricity prices.
Incorporating weather data.
Analysing renewable intermittency.
Modelling residual demand.
Developing electricity price forecasting models.
Investigating relationships between gas generation and market prices.
Developing potential energy trading signals.


### Step 3 — Save it
```text
docs/
└── methodology.md
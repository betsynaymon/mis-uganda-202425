# DHS Malaria Indicator Survey ITN Access and Use Analysis
This repo analyzes the 2024-2025 DHS Malaria Inidicator Survey (MIS) to identify the rates of ITN access and usage by region. 

## Overview
The goal of this repo was to replicate the findings from the 2024-25 MIS that demonstrates that across all 15 sub-regions, ITN access consistently exceed use. This means that households have enough nets to cover all individuals in the household, but a meaningful share are not sleeping under them. The gap ranges from 13% in Toro to 1% in Lango. These figures were computed from raw DHS microdata and reconciled against the published MIS report. All 30 subregion estimates match the official values within one percentage point. 

![Reconciliation table comparing computed rates against published MIS rates] (images/comparison.png) 

## Data
DHS data is available from [[the DHS website](https://dhsprogram.com/Data/)] for free following registration. Within the Uganda 2024-2025 DHS-9 MIS data, the following datasets are used by this analysis:

- Household Member Recode (Stata datset) = `UGPR91DT.ZIP`
- Household Recode (State dataset) = `UGHR91DT.ZIP`
- Geographic dataset (Shp file) = `UGGE91FL.ZIP`

Note: `data/raw/` is git ignored due to DHS terms that prohibit redistribution of microdata.  

## Setup

```
pip install -r requirements.txt
```

## Usage
Run `01_analysis.ipynb` first, which reads the survey data and outputs `data/processed/access_use_rates.csv`. Then run `02_visualization.ipynb` which reads the processed CSV and GPS dataset and produces the maps. 

## Project Structure

```
├── data/
│   ├── raw/              # DHS microdata (gitignored)
│   └── processed/        # cleaned output CSVs
├── notebooks/
│   ├── 01_analysis.ipynb
│   └── 02_visualization.ipynb
├── .gitignore
├── README.md
└── requirements.txt
```

## License
MIT
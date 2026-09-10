import zipfile
import numpy as np
import pandas as pd

## Read in Household Member Recode & Household Recode ##
# Household member
HMRpath = "../data/raw/UGPR91DT.zip"

with zipfile.ZipFile(HMRpath) as zip_ref:
    zip_ref.extractall("../data/raw")
    print("Extracted files:")
    for file in zip_ref.namelist():
        print(file)

rawHMR = pd.read_stata("../data/raw/UGPR91FL.dta")
# Household
HRpath = "../data/raw/UGHR91DT.zip"

with zipfile.ZipFile(HRpath) as zip_ref:
    zip_ref.extractall("../data/raw")
    print("Extracted files:")
    for file in zip_ref.namelist():
        print(file)

rawHR= pd.read_stata("../data/raw/UGHR91FL.dta")

# Prep HMR
cols = ['hhid', 'hv001', 'hvidx', 'hv005', 'hv024', 'hv103', 'hmlidx',
        'hml10', 'hml12', 'hml1', 'hml1a']
hmr = rawHMR[cols]

# Filter to de facto household members
hmr_df = hmr[hmr['hv103'] == 'yes'].copy()
records_dropped = len(hmr) - len(hmr_df)
print("Records dropped:", records_dropped)

######### ITN Use by Region ########
# The sample design of the 2024-2025 Uganda MIS separates sampling frames
# for refugee settlements and non-refugee areas. Therefore the weights are
# calibrated to make the non-refugee sample representative of the non-
# refugee Ugandan population. 

# Use = weighted sum of "slept under ITN" / weighted sum of all de
# facto members

# Create "slept under ITN column"
ITN_pos = ['only treated (itn) nets', 'both treated (itn) and untreated nets']
hmr_df['slept_ITN'] = hmr_df['hml12'].isin(ITN_pos)

# Numerator = slept_ITN x weight
hmr_df['use_numerator'] = hmr_df.hv005 * hmr_df.slept_ITN

# Group by region
region_df = (hmr_df[['hv024', 'hv005', 'slept_ITN', 'use_numerator']]
    .groupby('hv024')
    .sum()
    .reset_index()
)

# Drop refugee settlements
region_df = region_df[region_df['hv005'] != 0]

region_df['use_rate'] = region_df['use_numerator']/region_df['hv005']

###### ITN access by region ######
# Build net-level dataset
#nets_df = hmr_df[['hhid', 'hml10', 'hmlidx']]
#nets_df = nets_df.dropna(subset='hmlidx').drop_duplicates(
#    subset=['hhid', 'hmlidx']
#)
#itn_counts = ()

# Total ITNs must be counted from Household Recode

# Calculate total nets per household
hr_cols = ['hhid']
hml10 = list(rawHR.filter(like='hml10'))
hr_cols.extend(hml10)

hr_df = rawHR[hr_cols].copy()
hr_df['total_itns'] = (hr_df[hml10] == 'yes').sum(axis=1)

total_itns_df = hr_df[['hhid', 'total_itns']]

hmr_df = hmr_df.merge(total_itns_df, how='left', on='hhid')

# ITN capacity
hmr_df['itn_capacity'] = hmr_df['total_itns'] * 2

# Household size
hh_df = hmr_df[['hhid', 'hvidx']]
size = hh_df.groupby('hhid')['hvidx'].nunique().reset_index()
size.columns = ['hhid', 'hh_size']

hmr_df = hmr_df.merge(size, how='left', on='hhid')

            
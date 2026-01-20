import pandas as pd

enrol = pd.read_csv('data/enrolment_merged_cleaned.csv')
enrol['date'] = pd.to_datetime(enrol['date'], format='%d-%m-%Y')

print(f'Before any filter - Total rows: {len(enrol):,}')
print(f'Before any filter - Total age_0_5: {enrol["age_0_5"].sum():,}')

enrol['year'] = enrol['date'].dt.year
print(f'\nDate range: {enrol["date"].min()} to {enrol["date"].max()}')
print(f'Unique years: {sorted(enrol["year"].unique())}')

print(f'\nBreakdown by year:')
for year in sorted(enrol['year'].unique()):
    year_data = enrol[enrol['year'] == year]
    print(f'{year}: {len(year_data):,} rows, age_0_5 sum = {year_data["age_0_5"].sum():,}')

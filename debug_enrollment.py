import pandas as pd

enrol = pd.read_csv('data/enrolment_merged_cleaned.csv')
enrol['date'] = pd.to_datetime(enrol['date'], format='%d-%m-%Y')

print("=== DATA STRUCTURE ANALYSIS ===\n")

# Check if same pincode appears multiple times
sample_pincode = enrol.iloc[0]['pincode']
sample_state = enrol.iloc[0]['state']
pincode_entries = enrol[(enrol['pincode'] == sample_pincode) & (enrol['state'] == sample_state)]

print(f"Sample pincode: {sample_pincode} in {sample_state}")
print(f"Number of entries for this pincode: {len(pincode_entries)}")
print(pincode_entries[['date', 'pincode', 'age_0_5', 'age_5_17', 'age_18_greater']].to_string())

print("\n\n=== AGGREGATION COMPARISON ===\n")

# Compare different aggregation methods
print("Method 1: Sum ALL rows (what we should do if each row is unique enrollment)")
total_all = enrol['age_0_5'].sum()
print(f"Total age_0_5: {total_all:,}")

print("\n\nMethod 2: Latest date only per pincode (if data is cumulative)")
latest_per_pincode = enrol.sort_values('date').groupby(['state', 'district', 'pincode']).tail(1)
total_latest = latest_per_pincode['age_0_5'].sum()
print(f"Total age_0_5: {total_latest:,}")
print(f"Number of unique pincodes: {len(latest_per_pincode):,}")

print("\n\nMethod 3: Latest YEAR only, sum all (current method in coverage_gap_analysis)")
enrol['year'] = enrol['date'].dt.year
latest_year = enrol['year'].max()
latest_year_data = enrol[enrol['year'] == latest_year]
total_latest_year = latest_year_data['age_0_5'].sum()
print(f"Latest year: {latest_year}")
print(f"Total age_0_5: {total_latest_year:,}")

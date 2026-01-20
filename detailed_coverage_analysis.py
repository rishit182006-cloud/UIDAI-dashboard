import pandas as pd
import numpy as np
import sys

# Set UTF-8 encoding for output
sys.stdout.reconfigure(encoding='utf-8')

print("="*80)
print("DETAILED COVERAGE ANALYSIS - Finding the Gaps")
print("="*80)

# Load enrollment data
print("\n1. Loading enrollment data...")
enrol = pd.read_csv('data/enrolment_merged_cleaned.csv')
enrol['date'] = pd.to_datetime(enrol['date'], format='%d-%m-%Y')

print(f"   Total records: {len(enrol):,}")
print(f"   Date range: {enrol['date'].min()} to {enrol['date'].max()}")

# Calculate total enrollments by age group
print("\n2. Total Enrollments by Age Group:")
print("="*80)
total_0_5 = enrol['age_0_5'].sum()
total_5_17 = enrol['age_5_17'].sum()
total_18_above = enrol['age_18_greater'].sum()
grand_total = total_0_5 + total_5_17 + total_18_above

print(f"   Age 0-5:       {total_0_5:>15,}")
print(f"   Age 5-17:      {total_5_17:>15,}")
print(f"   Age 18+:       {total_18_above:>15,}")
print(f"   {'─'*40}")
print(f"   GRAND TOTAL:   {grand_total:>15,}")

# Load population data to compare
print("\n3. Loading Population Data for Comparison...")
print("="*80)

# Try to find population file
import os
pop_files = [
    'data/population.csv',
    'data/population_data.csv',
    'data/census.csv',
    'data/state_population.csv'
]

pop_df = None
for f in pop_files:
    if os.path.exists(f):
        print(f"   Found population file: {f}")
        pop_df = pd.read_csv(f)
        break

if pop_df is not None:
    print(f"   Population file columns: {list(pop_df.columns)}")
    print(f"   Population file rows: {len(pop_df):,}")
    
    # Check what population columns exist
    if 'total_population' in pop_df.columns:
        total_pop = pop_df['total_population'].sum()
        print(f"\n   Total Population: {total_pop:>15,}")
        coverage_pct = (grand_total / total_pop) * 100
        print(f"   Coverage %:       {coverage_pct:>14.2f}%")
        print(f"\n   ⚠️  Expected government coverage: 80%+")
        print(f"   ⚠️  Current coverage: {coverage_pct:.2f}%")
        print(f"   ⚠️  GAP: {80 - coverage_pct:.2f}%")
    
    # Show first few rows
    print("\n   Sample population data:")
    print(pop_df.head())
else:
    print("   ⚠️  No population file found!")
    print("   ⚠️  Cannot calculate accurate coverage without population data")

# State-wise analysis
print("\n4. State-wise Enrollment Analysis:")
print("="*80)

state_enrollment = enrol.groupby('state').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
}).reset_index()

state_enrollment['total'] = (state_enrollment['age_0_5'] + 
                              state_enrollment['age_5_17'] + 
                              state_enrollment['age_18_greater'])

state_enrollment = state_enrollment.sort_values('total', ascending=False)

print("\nTop 10 States by Total Enrollment:")
print(f"{'State':<30} {'Total':>15} {'Age 0-5':>12} {'Age 5-17':>12} {'Age 18+':>12}")
print("─"*80)
for idx, row in state_enrollment.head(10).iterrows():
    print(f"{row['state']:<30} {row['total']:>15,.0f} {row['age_0_5']:>12,.0f} "
          f"{row['age_5_17']:>12,.0f} {row['age_18_greater']:>12,.0f}")

print("\nBottom 10 States by Total Enrollment (POTENTIAL GAPS):")
print(f"{'State':<30} {'Total':>15} {'Age 0-5':>12} {'Age 5-17':>12} {'Age 18+':>12}")
print("─"*80)
for idx, row in state_enrollment.tail(10).iterrows():
    print(f"{row['state']:<30} {row['total']:>15,.0f} {row['age_0_5']:>12,.0f} "
          f"{row['age_5_17']:>12,.0f} {row['age_18_greater']:>12,.0f}")

# Temporal analysis
print("\n5. Enrollment Over Time:")
print("="*80)

enrol['year'] = enrol['date'].dt.year
yearly_enrollment = enrol.groupby('year').agg({
    'age_0_5': 'sum',
    'age_5_17': 'sum',
    'age_18_greater': 'sum'
}).reset_index()

yearly_enrollment['total'] = (yearly_enrollment['age_0_5'] + 
                               yearly_enrollment['age_5_17'] + 
                               yearly_enrollment['age_18_greater'])

print(f"\n{'Year':<10} {'Total':>15} {'Age 0-5':>12} {'Age 5-17':>12} {'Age 18+':>12}")
print("─"*80)
for idx, row in yearly_enrollment.iterrows():
    print(f"{row['year']:<10} {row['total']:>15,.0f} {row['age_0_5']:>12,.0f} "
          f"{row['age_5_17']:>12,.0f} {row['age_18_greater']:>12,.0f}")

# Check for missing data patterns
print("\n6. Data Quality Checks:")
print("="*80)

# Check for zeros
zero_counts = {
    'age_0_5': (enrol['age_0_5'] == 0).sum(),
    'age_5_17': (enrol['age_5_17'] == 0).sum(),
    'age_18_greater': (enrol['age_18_greater'] == 0).sum()
}

print(f"\nRecords with ZERO values:")
for col, count in zero_counts.items():
    pct = (count / len(enrol)) * 100
    print(f"   {col:<15}: {count:>8,} records ({pct:>5.1f}%)")

# Check for very small values
print(f"\nRecords with VERY SMALL values (< 10):")
for col in ['age_0_5', 'age_5_17', 'age_18_greater']:
    count = (enrol[col] < 10).sum()
    pct = (count / len(enrol)) * 100
    print(f"   {col:<15}: {count:>8,} records ({pct:>5.1f}%)")

# Average enrollments per record
print(f"\nAverage enrollments per record:")
for col in ['age_0_5', 'age_5_17', 'age_18_greater']:
    avg = enrol[col].mean()
    median = enrol[col].median()
    print(f"   {col:<15}: mean={avg:>10,.1f}, median={median:>10,.1f}")

# Check distribution
print(f"\nEnrollment distribution statistics:")
print(enrol[['age_0_5', 'age_5_17', 'age_18_greater']].describe())

# CRITICAL: Check if enrollments are cumulative or incremental
print("\n7. CRITICAL CHECK: Are enrollments cumulative or incremental?")
print("="*80)
print(f"\nIf enrollment data represents DAILY/PERIODIC additions (incremental):")
print(f"   ✓ We should SUM all records to get total enrolled")
print(f"   ✓ Current approach: CORRECT")
print(f"\nIf enrollment data represents CUMULATIVE counts at each date:")
print(f"   ✗ We should take ONLY the LATEST date's values")
print(f"   ✗ Current approach: WRONG - we're over-counting")

# Check if values are increasing over time for same state
print(f"\nSampling a state to check pattern - let's look at a specific state over time:")
sample_state = state_enrollment.iloc[0]['state']
state_sample = enrol[enrol['state'] == sample_state].sort_values('date').head(20)
print(f"\nState: {sample_state}")
print(f"First 20 records sorted by date:")
print(state_sample[['date', 'age_0_5', 'age_5_17', 'age_18_greater']])

# Summary and recommendations
print("\n" + "="*80)
print("SUMMARY AND LIKELY ISSUES:")
print("="*80)
print("""
Based on this analysis, the low coverage could be due to:

1. ⚠️  INCREMENTAL vs CUMULATIVE DATA INTERPRETATION
   - If the data is cumulative (each row = total enrolled as of that date),
     we're MASSIVELY over-counting by summing all rows
   - Solution: Take only the MAXIMUM date's values per state

2. ⚠️  MISSING POPULATION DATA
   - Without accurate population data, we can't calculate true coverage
   - Need to ensure population file matches enrollment data granularity

3. ⚠️  DATA QUALITY ISSUES
   - Check if there are many zero or very small enrollment values
   - May indicate incomplete data collection

4. ⚠️  TIME PERIOD MISMATCH
   - Enrollment data date range may not match population census year
   - Need to align temporal coverage

5. ⚠️  GEOGRAPHIC COVERAGE GAPS
   - Some states may have very low enrollment
   - Check if all states/districts are represented

RECOMMENDATION:
Review the data source documentation to confirm whether enrollment_merged_cleaned.csv
contains INCREMENTAL (daily additions) or CUMULATIVE (running totals) data.
""")

print("\n" + "="*80)
print("Analysis complete!")
print("="*80)

"""
Test script to verify enrollment aggregation after fix
"""
import pandas as pd
from utils import load_data, load_birth_data, normalize_state_names
from analysis import coverage_gap_analysis

print("="*70)
print("VERIFICATION: Enrollment Aggregation Fix")
print("="*70)

# Load unfiltered data
enrol, _, _ = load_data()
birth_df = load_birth_data()

print(f"\n1. RAW DATA CHECK:")
print(f"   Total rows in enrollment CSV: {len(enrol):,}")
print(f"   Sum of all age_0_5 enrollments: {enrol['age_0_5'].sum():,}")
print(f"   Date range: {enrol['date'].min().date()} to {enrol['date'].max().date()}")

print(f"\n2. BIRTH DATA:")
print(f"   Total annual births (all states): {birth_df['total_births'].sum():,}")

print(f"\n3. RUNNING coverage_gap_analysis()...")
fig, gap_df = coverage_gap_analysis(enrol, birth_df)

print(f"\n4. RESULTS:")
print(f"   Total enrolled_0_5 in analysis: {gap_df['enrolled_0_5'].sum():,}")
print(f"   Total births in analysis: {gap_df['total_births'].sum():,}")
overall_gap = ((gap_df['total_births'].sum() - gap_df['enrolled_0_5'].sum()) / gap_df['total_births'].sum() * 100)
print(f"   Overall coverage: {100 - overall_gap:.1f}%")
print(f"   Overall gap: {overall_gap:.1f}%")

print(f"\n5. TOP 5 STATES WITH LOWEST COVERAGE:")
top_gaps = gap_df.nlargest(5, 'coverage_gap_percent')[['state', 'total_births', 'enrolled_0_5', 'coverage_gap_percent']]
print(top_gaps.to_string(index=False))

print(f"\n6. STATES WITH BEST COVERAGE:")
best = gap_df.nsmallest(5, 'coverage_gap_percent')[['state', 'total_births', 'enrolled_0_5', 'coverage_gap_percent']]
print(best.to_string(index=False))

print("\n" + "="*70)
print("✓ Verification complete!")
print("="*70)

import pandas as pd
from utils import load_data, load_birth_data

enrol, _, _ = load_data()
birth_df = load_birth_data()

print("="*60)
print("UNDERSTANDING THE DATA MISMATCH")
print("="*60)

# The birth data total
total_births = birth_df['total_births'].sum()
print(f"\nTotal births in govt data: {total_births:,}")
print("  ^ These represent ANNUAL births (births per year)")

# The enrollment data
total_enrol = enrol['age_0_5'].sum()
print(f"\nTotal age_0_5 enrollment in UIDAI data: {total_enrol:,}")
print(f"  ^ These represent enrollments from {enrol['date'].min().date()} to {enrol['date'].max().date()}")
print(f"  ^ That's approximately {(enrol['date'].max() - enrol['date'].min()).days} days")

# The issue
print(f"\n{'='*60}")
print("THE PROBLEM:")
print("="*60)
print("\nWe're comparing:")
print(f"  - Annual births (per year): ~{total_births/1000000:.1f}M")
print(f"  - Enrollments over ~10 months: ~{total_enrol/1000000:.1f}M")
print("\nThis is like comparing apples to oranges!")

print(f"\n{'='*60}")
print("POTENTIAL INTERPRETATIONS:")
print("="*60)

print("\n1. If enrollment data represents NEW enrollments per day:")
print(f"   Total enrollments: {total_enrol:,}")
print(f"   Coverage vs annual births: {(total_enrol/total_births*100):.1f}%")

print("\n2. If each row represents CUMULATIVE enrollments at that pincode:")
print("   We should only use the LATEST date per pincode")
latest_per_pincode = enrol.sort_values('date').groupby(['state', 'district', 'pincode']).tail(1)
total_latest = latest_per_pincode['age_0_5'].sum()
print(f"   Total enrollments: {total_latest:,}")
print(f"   Coverage vs annual births: {(total_latest/total_births*100):.1f}%")

print("\n3. If we should compare to cumulative births over 5 years (0-5 age group):")
cumulative_births_5yr = total_births * 5
print(f"   Cumulative births over 5 years: {cumulative_births_5yr:,}")
print(f"   Coverage: {(total_enrol/cumulative_births_5yr*100):.1f}%")

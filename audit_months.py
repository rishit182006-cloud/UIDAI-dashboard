import pandas as pd
import numpy as np

def check_august():
    print("Reading enrollment data...")
    # Read only needed columns to be fast
    df = pd.read_csv('data/enrolment_merged_cleaned.csv')
    
    # Convert date and handle potential errors
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y', errors='coerce')
    
    # Drop rows where date couldn't be parsed
    initial_count = len(df)
    df = df.dropna(subset=['date'])
    if len(df) < initial_count:
        print(f"Dropped {initial_count - len(df)} rows with invalid dates.")

    # Extract month and year
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    
    # Perform aggregation
    print("\nAggregating by month...")
    summary = df.groupby(['year', 'month']).agg(
        record_count=('state', 'count'),
        age_0_5=('age_0_5', 'sum'),
        age_5_17=('age_5_17', 'sum'),
        age_18_greater=('age_18_greater', 'sum')
    ).reset_index()
    
    # Add month names
    month_map = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April',
        5: 'May', 6: 'June', 7: 'July', 8: 'August',
        9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }
    summary['month_name'] = summary['month'].map(month_map)
    
    print("\nEnrollment Data Audit (2025):")
    print("="*80)
    cols = ['year', 'month_name', 'record_count', 'age_0_5', 'age_5_17', 'age_18_greater']
    print(summary[cols].sort_values(['year', 'month']).to_string(index=False))
    
    # Specifically check August
    aug_data = df[df['month'] == 8]
    print(f"\nAugust Specific Check:")
    print(f"Total records in August: {len(aug_data)}")
    
    if len(aug_data) == 0:
        print("\nCONCLUSION: There is NO DATA for August in the source file.")
        print("The data jumps directly from July to September.")
    else:
        print(f"August Sums: {aug_data[['age_0_5', 'age_5_17', 'age_18_greater']].sum()}")

if __name__ == "__main__":
    check_august()

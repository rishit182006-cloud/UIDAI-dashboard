"""
Enhanced Metrics for Enrollment Data Analysis

This module provides meaningful metrics for INCREMENTAL enrollment data,
focusing on velocity, trends, and comparative performance rather than
absolute coverage percentages.
"""

import pandas as pd
import numpy as np


def load_enrollment_data(filepath='data/enrolment_merged_cleaned.csv'):
    """Load and prepare enrollment data"""
    df = pd.read_csv(filepath)
    df['date'] = pd.to_datetime(df['date'], format='%d-%m-%Y')
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['month_name'] = df['date'].dt.strftime('%B')
    df['week'] = df['date'].dt.isocalendar().week
    df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
    return df


def calculate_enrollment_velocity(df):
    """Calculate enrollment rates over time"""
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df = df.copy()
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
    # Ensure temporal columns exist
    if 'year' not in df.columns:
        df = df.copy()
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        df['month_name'] = df['date'].dt.strftime('%B')
        df['week'] = df['date'].dt.isocalendar().week
        
    # Daily enrollment rates
    daily = df.groupby('date').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum', 
        'age_18_greater': 'sum',
        'total_enrollments': 'sum'
    }).reset_index()
    
    # Monthly enrollment rates
    monthly = df.groupby(['year', 'month', 'month_name']).agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrollments': 'sum'
    }).reset_index()
    monthly['year_month'] = monthly['year'].astype(str) + '-' + monthly['month'].astype(str).str.zfill(2)
    
    # Weekly enrollment rates
    weekly = df.groupby(['year', 'week']).agg({
        'total_enrollments': 'sum'
    }).reset_index()
    weekly['year_week'] = weekly['year'].astype(str) + '-W' + weekly['week'].astype(str).str.zfill(2)
    
    return {
        'daily': daily,
        'monthly': monthly,
        'weekly': weekly
    }


def calculate_state_performance(df):
    """Calculate state performance metrics normalized by districts"""
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df = df.copy()
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
    state_stats = df.groupby('state').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrollments': 'sum',
        'district': 'nunique',  # Number of unique districts
        'pincode': 'nunique'     # Number of unique pincodes
    }).reset_index()
    
    state_stats.rename(columns={'district': 'num_districts', 'pincode': 'num_pincodes'}, inplace=True)
    
    # Performance index: enrollments per district (normalizes for state size)
    state_stats['enrollments_per_district'] = (
        state_stats['total_enrollments'] / state_stats['num_districts']
    ).round(0)
    
    # Age group focus percentages
    state_stats['pct_children_0_5'] = (
        (state_stats['age_0_5'] / state_stats['total_enrollments']) * 100
    ).round(1)
    
    state_stats['pct_children_5_17'] = (
        (state_stats['age_5_17'] / state_stats['total_enrollments']) * 100
    ).round(1)
    
    state_stats['pct_adults'] = (
        (state_stats['age_18_greater'] / state_stats['total_enrollments']) * 100
    ).round(1)
    
    # Sort by performance index
    state_stats = state_stats.sort_values('enrollments_per_district', ascending=False)
    
    return state_stats


def calculate_district_performance(df):
    """Calculate top performing districts nationally"""
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df = df.copy()
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
    district_stats = df.groupby(['state', 'district']).agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum',
        'total_enrollments': 'sum',
        'pincode': 'nunique'
    }).reset_index()
    
    district_stats.rename(columns={'pincode': 'num_pincodes'}, inplace=True)
    
    # Enrollments per pincode (activity density)
    district_stats['enrollments_per_pincode'] = (
        district_stats['total_enrollments'] / district_stats['num_pincodes']
    ).round(0)
    
    # Sort by total enrollments
    district_stats = district_stats.sort_values('total_enrollments', ascending=False)
    
    return district_stats


def calculate_temporal_trends(df):
    """Analyze temporal patterns and trends"""
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df = df.copy()
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
    # Ensure temporal columns exist
    if 'year' not in df.columns:
        df = df.copy()
        df['year'] = df['date'].dt.year
        df['month'] = df['date'].dt.month
        
    # Month-over-month growth
    monthly = df.groupby(['year', 'month']).agg({
        'total_enrollments': 'sum'
    }).reset_index()
    
    monthly['prev_month'] = monthly['total_enrollments'].shift(1)
    monthly['mom_growth'] = ((monthly['total_enrollments'] - monthly['prev_month']) / 
                              monthly['prev_month'] * 100).round(1)
    monthly['month_name'] = pd.to_datetime(monthly['month'], format='%m').dt.strftime('%B')
    
    # Day of week patterns
    df['day_of_week'] = df['date'].dt.day_name()
    dow_pattern = df.groupby('day_of_week')['total_enrollments'].sum().reset_index()
    
    # Peak enrollment periods
    top_days = df.groupby('date')['total_enrollments'].sum().nlargest(10).reset_index()
    
    return {
        'monthly_growth': monthly,
        'day_of_week_pattern': dow_pattern,
        'peak_days': top_days
    }


def get_age_distribution_by_state(df):
    """Get age group distribution for each state"""
    
    age_dist = df.groupby('state').agg({
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    
    # Melt for easier visualization
    age_dist_melted = age_dist.melt(
        id_vars=['state'],
        value_vars=['age_0_5', 'age_5_17', 'age_18_greater'],
        var_name='age_group',
        value_name='enrollments'
    )
    
    return age_dist_melted


def get_summary_statistics(df):
    """Calculate summary statistics for the dataset"""
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df = df.copy()
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
    total_enrollments = df['total_enrollments'].sum()
    date_range_days = (df['date'].max() - df['date'].min()).days
    avg_daily = total_enrollments / date_range_days if date_range_days > 0 else 0
    
    # Ensure date has required columns if missing
    if 'year' not in df.columns:
        df['year'] = df['date'].dt.year
        
    num_states = df['state'].nunique()
    num_districts = df['district'].nunique()
    num_pincodes = df['pincode'].nunique()
    
    return {
        'total_enrollments': int(total_enrollments),
        'age_0_5': int(df['age_0_5'].sum()),
        'age_5_17': int(df['age_5_17'].sum()),
        'age_18_greater': int(df['age_18_greater'].sum()),
        'date_range': f"{df['date'].min().date()} to {df['date'].max().date()}",
        'date_range_days': date_range_days,
        'avg_daily_enrollments': int(avg_daily),
        'num_states': num_states,
        'num_districts': num_districts,
        'num_pincodes': num_pincodes,
        'num_records': len(df)
    }


def calculate_population_coverage(df, pop_df):
    """Calculates enrollment relative to population for each state"""
    from utils import normalize_state_names
    df = normalize_state_names(df.copy())
    pop_df = normalize_state_names(pop_df.copy())
    
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
    state_totals = df.groupby('state')['total_enrollments'].sum().reset_index()
    merged = pd.merge(state_totals, pop_df, on='state', how='inner')
    
    # Calculate ratio (enrollments per person)
    merged['enrollment_ratio'] = merged['total_enrollments'] / merged['Population']
    # Calculate enrollments per 100k people for better scale
    merged['enrollments_per_100k'] = (merged['total_enrollments'] / merged['Population']) * 100000
    
    return merged.sort_values('enrollment_ratio', ascending=False)


def calculate_adult_enrollment_by_state(df):
    """Calculates total adult enrollment by state"""
    from utils import normalize_state_names
    df = normalize_state_names(df.copy())
    
    adult_stats = df.groupby('state')['age_18_greater'].sum().reset_index()
    return adult_stats.sort_values('age_18_greater', ascending=False)


def get_top_pincodes(df, top_n=50):
    """Get top performing pincodes by enrollment volume"""
    # Ensure total_enrollments exists
    if 'total_enrollments' not in df.columns:
        df = df.copy()
        df['total_enrollments'] = df['age_0_5'] + df['age_5_17'] + df['age_18_greater']
        
    pincode_stats = df.groupby(['state', 'district', 'pincode']).agg({
        'total_enrollments': 'sum',
        'age_0_5': 'sum',
        'age_5_17': 'sum',
        'age_18_greater': 'sum'
    }).reset_index()
    
    pincode_stats = pincode_stats.sort_values('total_enrollments', ascending=False).head(top_n)
    
    return pincode_stats


if __name__ == '__main__':
    # Test the metrics
    print("Loading enrollment data...")
    df = load_enrollment_data()
    
    print("\n" + "="*80)
    print("SUMMARY STATISTICS")
    print("="*80)
    stats = get_summary_statistics(df)
    for key, value in stats.items():
        print(f"{key:.<40} {value}")
    
    print("\n" + "="*80)
    print("TOP 10 STATES BY PERFORMANCE INDEX (Enrollments per District)")
    print("="*80)
    state_perf = calculate_state_performance(df)
    print(state_perf[['state', 'total_enrollments', 'num_districts', 
                      'enrollments_per_district', 'pct_children_0_5']].head(10).to_string(index=False))
    
    print("\n" + "="*80)
    print("TOP 10 DISTRICTS BY TOTAL ENROLLMENTS")
    print("="*80)
    district_perf = calculate_district_performance(df)
    print(district_perf[['state', 'district', 'total_enrollments', 
                         'enrollments_per_pincode']].head(10).to_string(index=False))
    
    print("\n" + "="*80)
    print("MONTHLY ENROLLMENT TRENDS")
    print("="*80)
    velocity = calculate_enrollment_velocity(df)
    print(velocity['monthly'][['year_month', 'month_name', 'total_enrollments']].to_string(index=False))
    
    print("\n✓ Enhanced metrics module is working correctly!")

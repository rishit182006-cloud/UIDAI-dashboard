import plotly.express as px
import pandas as pd
import numpy as np
from enhanced_metrics import (
    calculate_enrollment_velocity,
    calculate_state_performance,
    calculate_district_performance,
    get_age_distribution_by_state,
    calculate_population_coverage,
    calculate_adult_enrollment_by_state
)

def enrollment_trend(enrol):
    """Line chart showing daily enrollment volume across age groups"""
    # Ensure date is datetime
    if not pd.api.types.is_datetime64_any_dtype(enrol['date']):
        enrol['date'] = pd.to_datetime(enrol['date'], format='%d-%m-%Y')
    
    trend = enrol.groupby('date')[['age_0_5','age_5_17','age_18_greater']].sum().reset_index()
    fig = px.line(trend, x='date', y=['age_0_5','age_5_17','age_18_greater'],
                  title="Daily Enrollment Trend (New 2025 Enrollments)",
                  labels={"value": "Count", "date": "Date", "variable": "Age Group"},
                  color_discrete_sequence=px.colors.qualitative.Safe)
    fig.update_layout(hovermode="x unified")
    return fig

def monthly_velocity_chart(enrol):
    """Bar chart showing enrollment volume per month"""
    velocity_data = calculate_enrollment_velocity(enrol)
    monthly = velocity_data['monthly']
    
    fig = px.bar(monthly, x='month_name', y='total_enrollments',
                 title="Enrollment Velocity by Month (2025)",
                 labels={"total_enrollments": "Total New Enrollments", "month_name": "Month"},
                 text_auto='.2s',
                 color='total_enrollments',
                 color_continuous_scale='Viridis')
    fig.update_layout(xaxis={'categoryorder':'array', 'categoryarray':['March','April','May','June','July','August','September','October','November','December']})
    return fig

def state_performance_ranking(enrol):
    """Horizontal bar chart showing enrollments per district (Normalized Performance)"""
    state_perf = calculate_state_performance(enrol)
    top_states = state_perf.head(15)
    
    fig = px.bar(top_states, 
                 y='state', x='enrollments_per_district',
                 title="State Performance: Enrollments per District (Normalized)",
                 orientation='h',
                 labels={"enrollments_per_district": "Enrollments per District", "state": "State"},
                 color='enrollments_per_district',
                 color_continuous_scale='Tealgrn')
    fig.update_layout(yaxis={'categoryorder':'total ascending'})
    return fig

def district_leaderboard(enrol):
    """Bar chart for top 20 districts nationally"""
    dist_perf = calculate_district_performance(enrol).head(20)
    
    fig = px.bar(dist_perf, 
                 x='district', y='total_enrollments',
                 title="Top 20 Districts by New Enrollments (National)",
                 labels={"total_enrollments": "Total Enrollments", "district": "District"},
                 color='total_enrollments',
                 hover_data=['state'],
                 color_continuous_scale='Blues')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def age_group_composition(enrol):
    """Stacked bar chart showing age group distribution by state"""
    age_dist = get_age_distribution_by_state(enrol)
    
    # Calculate totals for sorting
    totals = age_dist.groupby('state')['enrollments'].sum().reset_index()
    top_states = totals.sort_values('enrollments', ascending=False).head(15)['state'].tolist()
    age_dist_top = age_dist[age_dist['state'].isin(top_states)]
    
    fig = px.bar(age_dist_top, x='state', y='enrollments', color='age_group',
                 title="Age Group Composition in Top 15 States",
                 labels={"enrollments": "New Enrollments", "state": "State", "age_group": "Age Group"},
                 barmode='stack',
                 color_discrete_map={
                     'age_0_5': '#1f77b4',
                     'age_5_17': '#ff7f0e',
                     'age_18_greater': '#2ca02c'
                 })
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

def age_distribution(enrol):
    """Pie chart for global age group distribution"""
    age_sum = enrol[['age_0_5','age_5_17','age_18_greater']].sum().reset_index()
    age_sum.columns = ['Age Group', 'Total']
    fig = px.pie(age_sum, names='Age Group', values='Total', 
                 title="National Age Group Distribution (New Enrollments)",
                 hole=0.4,
                 color_discrete_sequence=px.colors.qualitative.Pastel)
    return fig

def state_wise_enrollment(enrol):
    """Bar chart for total enrollment by state"""
    state_data = enrol.groupby('state')[['age_0_5', 'age_5_17', 'age_18_greater']].sum().reset_index()
    state_data['total'] = state_data['age_0_5'] + state_data['age_5_17'] + state_data['age_18_greater']
    
    fig = px.bar(state_data.sort_values('total', ascending=False).head(15),
                 x='state', y='total',
                 title="Top 15 States by New Enrollments (2025)",
                 labels={"total": "Total New Enrollments", "state": "State"},
                 color='total',
                 color_continuous_scale='Reds')
    return fig

def enrollment_vs_birth_scatter(enrol, birth_df):
    """Scatter plot: New Child Enrollments vs Total Births"""
    # Total enrollment per state
    enrol_state = enrol.groupby('state')[['age_0_5']].sum().reset_index()
    enrol_state.columns = ['state', 'enrolled_0_5']

    # Merge with birth data
    df = pd.merge(birth_df, enrol_state, on='state', how='inner')

    # Scatter plot
    fig = px.scatter(
        df,
        x='total_births',
        y='enrolled_0_5',
        text='state',
        title="2025 Child Enrollment Velocity vs State Birth Capacity",
        labels={
            "total_births": "Annual Registered Births (Base Capacity)",
            "enrolled_0_5": "Actual New Child Enrollments (UIDAI)"
        },
        trendline="ols"
    )

    fig.update_traces(textposition='top center')
    return fig

def coverage_gap_analysis(enrol, birth_df):
    """Bar chart: Gap between expected birth capacity and actual 2025 enrollments"""
    from utils import normalize_state_names
    enrol = normalize_state_names(enrol.copy())
    birth_df = normalize_state_names(birth_df.copy())

    state_totals = enrol.groupby('state', as_index=False).agg({'age_0_5': 'sum'})
    state_totals.rename(columns={'age_0_5': 'enrolled_0_5'}, inplace=True)

    df = pd.merge(birth_df, state_totals, on='state', how='left')
    df['enrolled_0_5'] = df['enrolled_0_5'].fillna(0)

    # Note: This is now interpreted as "Capacity Gap" - how many more enrollments 
    # we could expect based on birth rates.
    df['gap_pct'] = ((df['total_births'] - df['enrolled_0_5']) / df['total_births']) * 100
    df['gap_pct'] = df['gap_pct'].clip(0, 100)

    worst = df.sort_values('gap_pct', ascending=False).head(10)

    fig = px.bar(
        worst,
        x='state',
        y='gap_pct',
        text=worst['gap_pct'].round(1),
        title="State-wise Outreach Need (Births vs 2025 Enrollments)",
        labels={'gap_pct': '% of Expected Birth Capacity Unmet by 2025 Data'}
    )
    fig.update_traces(textposition='outside')
    return fig, worst


def population_coverage_chart(enrol, pop_df):
    """Horizontal bar chart showing enrollment / population ratio (Top States)"""
    coverage_data = calculate_population_coverage(enrol, pop_df)
    
    # Take top 15 for the chart
    top_coverage = coverage_data.head(15)
    
    fig = px.bar(top_coverage, 
                 y='state', x='enrollments_per_100k',
                 title="Performance Leaders: Enrollment Density (New Enrollments per 100k Population)",
                 orientation='h',
                 labels={"enrollments_per_100k": "Enrollments per 100k People", "state": "State"},
                 color='enrollments_per_100k',
                 color_continuous_scale='Sunsetdark',
                 text_auto='.2s')
    
    fig.update_layout(
        yaxis={'categoryorder':'total ascending', 'tickfont': {'color': 'blue'}},
        margin=dict(l=150)
    )
    return fig


def bottom_population_coverage_chart(enrol, pop_df):
    """Horizontal bar chart showing enrollment / population ratio (Bottom States)"""
    coverage_data = calculate_population_coverage(enrol, pop_df)
    
    # Take bottom 15 for the chart (excluding ones with 0 if they clutter)
    bottom_coverage = coverage_data.tail(15)
    
    fig = px.bar(bottom_coverage, 
                 y='state', x='enrollments_per_100k',
                 title="Performance Laggards: Enrollment Density (Lowest Enrollments per 100k Population)",
                 orientation='h',
                 labels={"enrollments_per_100k": "Enrollments per 100k People", "state": "State"},
                 color='enrollments_per_100k',
                 color_continuous_scale='OrRd',
                 text_auto='.2s')
    
    fig.update_layout(
        yaxis={'categoryorder':'total descending', 'tickfont': {'color': 'blue'}},
        margin=dict(l=150)
    )
    return fig


def adult_enrollment_by_state_chart(enrol):
    """Bar chart showing total adult enrollment by state"""
    adult_data = calculate_adult_enrollment_by_state(enrol).head(15)
    
    fig = px.bar(adult_data, 
                 x='state', y='age_18_greater',
                 title="Total New Adult Enrollments by State (Top 15)",
                 labels={"age_18_greater": "Adult Enrollments (18+)", "state": "State"},
                 color='age_18_greater',
                 color_continuous_scale='Purples')
    fig.update_layout(xaxis={'categoryorder':'total descending'})
    return fig

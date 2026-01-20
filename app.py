import streamlit as st
from utils import load_data, load_birth_data, load_population_data
from enhanced_metrics import get_summary_statistics
from analysis import (
    age_distribution,
    enrollment_trend,
    state_wise_enrollment,
    monthly_velocity_chart,
    age_group_composition,
    enrollment_vs_birth_scatter,
    population_coverage_chart,
    bottom_population_coverage_chart,
    adult_enrollment_by_state_chart
)

st.set_page_config(layout="wide", page_title="UIDAI 2025 Enrollment Insights")

# Load Data
enrol, bio, demo = load_data()
birth_df = load_birth_data()
pop_df = load_population_data()

# --- HEADER SECTION ---
st.title("📊 UIDAI 2025 Enrollment Analytics")
st.markdown("### *Focusing on New Enrollment Velocity and Regional Performance*")

# Summary Metrics
stats = get_summary_statistics(enrol)
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("Total 2025 Enrollments", f"{stats['total_enrollments']:,}")
with col2:
    st.metric("Avg Daily Velocity", f"{stats['avg_daily_enrollments']:,}/day")
with col3:
    st.metric("Primary Focus (Age 0-5)", f"{stats['age_0_5']:,}")
with col4:
    st.metric("Active Regions", f"{stats['num_districts']:,} Districts")

# --- SIDEBAR FILTERS ---
st.sidebar.header("🔍 Filters")
state_list = ["All"] + sorted(enrol['state'].dropna().unique().tolist())
selected_state = st.sidebar.selectbox("Select State", state_list)

filtered_enrol = enrol
if selected_state != "All":
    filtered_enrol = enrol[enrol['state'] == selected_state]

# --- MAIN DASHBOARD ---
tab1, tab2, tab3 = st.tabs(["📊 Performance Leaderboards", "🍼 Birth & Child Stats", "📅 Monthly Pulse"])

with tab1:
    st.subheader("Enrollment Density: Performance Leaders")
    st.plotly_chart(population_coverage_chart(enrol, pop_df), use_container_width=True)
    st.info("💡 High density indicates effective outreach relative to the total population baseline.")

    st.subheader("Enrollment Density: Performance Laggards")
    st.plotly_chart(bottom_population_coverage_chart(enrol, pop_df), use_container_width=True)
    st.warning("⚠️ These regions may require targeted registration awareness programs.")

    st.subheader("Adult Enrollment Leaderboard (18+)")
    st.plotly_chart(adult_enrollment_by_state_chart(enrol), use_container_width=True)

    st.subheader("Regional Age Distribution Focus (Top 15 States)")
    st.plotly_chart(age_group_composition(enrol), use_container_width=True)

with tab2:
    st.subheader("Child Enrollment (Age 0-5) Velocity vs Birth Capacity")
    st.plotly_chart(enrollment_vs_birth_scatter(filtered_enrol, birth_df), use_container_width=True)
    
    st.success("""
    **Analytical Note:** The scatter plot compares **Actual 2025 Momentum** against **State Birth Capacity**. 
    States falling significantly below the trend line (regression line) are priority zones for newborn enrollment.
    """)

with tab3:
    st.subheader("Monthly Enrollment Velocity (2025)")
    st.plotly_chart(monthly_velocity_chart(filtered_enrol), use_container_width=True)
    
    st.subheader("National Age Group Breakdown")
    st.plotly_chart(age_distribution(filtered_enrol), use_container_width=True)
    st.info("Peaks in the monthly velocity often correspond to government enrollment drives or school registration cycles.")

st.markdown("---")
st.caption(f"Data Source: enrolment_merged_cleaned.csv | Covering period: {stats['date_range']}")

import streamlit as st
from utils import load_data
from analysis import (
    age_distribution,
    enrollment_trend,
    state_wise_enrollment
)


st.set_page_config(layout="wide")
st.title("📊 UIDAI Data Insight Dashboard")

enrol, bio, demo = load_data()

st.sidebar.header("🔍 Filters")

state = st.sidebar.selectbox("Select State", ["All"] + sorted(enrol['state'].dropna().unique().tolist()))

if state != "All":
    enrol = enrol[enrol['state'] == state]
    bio = bio[bio['state'] == state]
    demo = demo[demo['state'] == state]

st.subheader("📈 Enrollment Trend")
st.plotly_chart(enrollment_trend(enrol), use_container_width=True)

st.subheader("🗺️ State-wise Enrollment")
st.plotly_chart(state_wise_enrollment(enrol), use_container_width=True)

st.subheader("Age Group Distribution")
st.plotly_chart(age_distribution(enrol), use_container_width=True, key="age_dist_full")





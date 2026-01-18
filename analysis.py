import plotly.express as px
import pandas as pd

def enrollment_trend(enrol):
    trend = enrol.groupby('date')[['age_0_5','age_5_17','age_18_greater']].sum().reset_index()
    fig = px.line(trend, x='date', y=trend.columns[1:],
                  title="Enrollment Trend Over Time")
    return fig

def state_wise_enrollment(enrol):
    state_data = enrol.groupby('state')['age_18_greater'].sum().reset_index()
    fig = px.bar(state_data.sort_values('age_18_greater', ascending=False).head(10),
                 x='state', y='age_18_greater',
                 title="Top 10 States by Adult Enrollment")
    return fig

def age_distribution(enrol):
    age_sum = enrol[['age_0_5','age_5_17','age_18_greater']].sum().reset_index()
    fig = px.pie(age_sum, names='index', values=0, title="Age Group Distribution")
    return fig



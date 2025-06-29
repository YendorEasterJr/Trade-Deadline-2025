
import streamlit as st
import pandas as pd
import numpy as np
import altair as alt

# Simulated trade data with extended analytics
data = {
    'Trade Target': [
        'Joey Meneses + Lane Thomas', 
        'Bryan De La Cruz', 
        'Luis Robert Jr.', 
        'Andrew McCutchen'
    ],
    'Team': ['Nationals', 'Marlins', 'White Sox', 'Pirates'],
    'WAR Gained': [1.3, 1.0, 1.4, 1.0],
    'Prospect Value': [42.5, 50, 53.3, 45],
    'MLB Asset Value': [40, 50, 50, 30],
    'Salary Cost (M USD)': [8.5, 0.86, 15.0, 5.0],
    'Control Years': [2, 3, 3, 0.5],
    '2026 Payroll Risk (M USD)': [3.5, 1.0, 17.5, 0],
    'Team Logo URL': [
        'https://a.espncdn.com/i/teamlogos/mlb/500/was.png',
        'https://a.espncdn.com/i/teamlogos/mlb/500/mia.png',
        'https://a.espncdn.com/i/teamlogos/mlb/500/chw.png',
        'https://a.espncdn.com/i/teamlogos/mlb/500/pit.png'
    ],
    'Playoff Odds Increase (%)': [3.2, 2.5, 4.1, 1.0]
}

df = pd.DataFrame(data)
df['Total Asset Cost'] = df['Prospect Value'] + df['MLB Asset Value']
df['WAR per Cost Unit'] = df['WAR Gained'] / df['Total Asset Cost']
df['Overall ROI'] = df['WAR per Cost Unit'] / df['Salary Cost (M USD)']

# Streamlit App UI
st.set_page_config(layout='wide')
st.title("🏆 Tampa Bay Rays Trade Strategy Dashboard")
st.markdown("Analyze middle-of-the-order trade targets based on WAR, ROI, control years, and playoff impact.")

# Filters
col1, col2 = st.columns(2)
with col1:
    min_war = st.slider("Minimum WAR Gained", 0.0, 2.0, 0.5, 0.1)
with col2:
    max_salary = st.slider("Maximum Salary Cost (M USD)", 0.0, 20.0, 15.0, 0.5)

filtered_df = df[(df['WAR Gained'] >= min_war) & (df['Salary Cost (M USD)'] <= max_salary)]

# Display filtered trades with visuals
st.subheader("🔍 Trade Target Profiles")
for _, row in filtered_df.iterrows():
    cols = st.columns([1, 4])
    with cols[0]:
        st.image(row['Team Logo URL'], width=60)
    with cols[1]:
        st.markdown(f"### {row['Trade Target']} ({row['Team']})")
        st.markdown(f"- **WAR Gained**: {row['WAR Gained']}")
        st.markdown(f"- **Salary**: ${row['Salary Cost (M USD)']}M")
        st.markdown(f"- **Control Years**: {row['Control Years']}")
        st.markdown(f"- **Payroll Risk 2026**: ${row['2026 Payroll Risk (M USD)']}M")
        st.markdown(f"- **Playoff Odds Boost**: {row['Playoff Odds Increase (%)']}%")
        st.markdown("---")

# ROI Chart
st.subheader("📊 ROI: WAR per Cost Unit vs Salary")
chart_data = filtered_df.copy()
chart_data['Trade Target'] = chart_data['Trade Target'].astype(str)
roi_chart = alt.Chart(chart_data).mark_bar().encode(
    x=alt.X('Trade Target', sort='-y'),
    y='Overall ROI',
    color=alt.Color('Salary Cost (M USD)', scale=alt.Scale(scheme='greens'))
).properties(height=400)
st.altair_chart(roi_chart, use_container_width=True)

# Heatmap for control years
st.subheader("🔥 Control Years Heatmap")
heatmap_data = filtered_df[['Trade Target', 'Control Years']]
heatmap_data = heatmap_data.set_index('Trade Target')
st.dataframe(heatmap_data.style.background_gradient(cmap='Oranges'))

# Scatter for WAR vs Asset Cost
st.subheader("⚖️ WAR vs Total Asset Cost")
scatter = alt.Chart(filtered_df).mark_circle(size=120).encode(
    x='Total Asset Cost',
    y='WAR Gained',
    tooltip=['Trade Target', 'WAR Gained', 'Total Asset Cost'],
    color=alt.Color('Playoff Odds Increase (%)', scale=alt.Scale(scheme='redyellowgreen')),
).interactive().properties(height=400)
st.altair_chart(scatter, use_container_width=True)

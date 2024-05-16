import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# ----------------------
# Data Loading & Preprocessing
# ----------------------
@st.cache_data
def load_data():
    return pd.read_parquet("app/gapminder_data.parquet")

merged_df = load_data()

# ----------------------
# Streamlit App
# ----------------------
merged_df = load_and_transform_df()

# Add Year Slider (after converting to numeric)
year_min = int(merged_df['year'].min())
year_max = int(merged_df['year'].max())
selected_year = st.slider("Year", year_min, year_max, year_max)

all_countries = sorted(merged_df['country'].unique())
selected_countries = st.multiselect("Countries", all_countries, default=all_countries)

# Filter Data based on year and selected countries
filtered_df = merged_df[
    (merged_df['year'] == selected_year) & (merged_df['country'].isin(selected_countries))
]

# Determine the maximum GNI value across all years to keep the x-axis fixed
max_gni = merged_df["GNI"].max()

# Create Bubble Chart
fig = px.scatter(
    filtered_df,
    x="GNI", y="LEX",
    size="POP", color="country",
    hover_name="country",
    log_x=True, size_max=60,
    title=f"Bubble Chart for {selected_year}",
    labels={"GNI": "Gross National Income per Capita (log scale)", "LEX": "Life Expectancy"},
    range_x=[0, max_gni * 1.1]  # Set the x-axis range to fix the max value
)

# Customize layout (optional)
fig.update_layout(
    xaxis_title="Gross National Income per Capita (log scale)",
    yaxis_title="Life Expectancy",
    showlegend=True,
)

# Display the Chart
st.plotly_chart(fig)

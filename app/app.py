import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# ----------------------
# Data Loading & Preprocessing
# ----------------------
def load_data():
    return pd.read_parquet("app/gapminder_data.parquet")

    # Convert columns to numeric (improved handling of missing values)
    melted_df[value_name] = (
        melted_df[value_name]
        .astype(str)
        .str.replace(r'[kMB]', '', regex=True)
        .str.replace(',', '.', regex=False)
        .replace('', '0')
        .astype(float)
    )
    melted_df[value_name] = melted_df[value_name].fillna(method='ffill')

    # Scale values
    melted_df[value_name] = melted_df[value_name].apply(
        lambda x: x * 1000 if x < 1000000 else (x * 1000000 if x < 1000000000 else x)
    )
    return melted_df

# Load and transform data
gni_df = load_and_transform_data("app/gni.csv", "GNI")
lex_df = load_and_transform_data("app/lex.csv", "LEX")
pop_df = load_and_transform_data("app/pop.csv", "POP")

# Merge dataframes 
merged_df = gni_df.merge(lex_df, on=['country', 'year']).merge(pop_df, on=['country', 'year'])
merged_df['year'] = pd.to_numeric(merged_df['year'],errors='coerce')

# ----------------------
# Streamlit App
# ----------------------

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

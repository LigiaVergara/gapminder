import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.graph_objects as go

st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# ----------------------
# Data Loading & Preprocessing
# ----------------------
@st.cache_data
def load_and_transform_df():
    """Loads all CSVs, processes them, and returns the merged DataFrame."""

    def load_and_transform_data(file_path, value_name):
        """Loads a CSV file, melts it, and standardizes relevant columns to numeric."""

        try:
            df = pd.read_csv(file_path)
            melted_df = pd.melt(df, id_vars=['country'], var_name='year', value_name=value_name)
            return melted_df

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None

    # Load and transform data
    

    script_dir = Path(__file__).resolve().parent

    # Construct the path to your CSV file
    file_gni = script_dir / "gni.csv"
    file_lex = script_dir / "lex.csv"
    file_pop = script_dir / "pop.csv"   
    gni_df = load_and_transform_data(file_gni, "GNI")
    lex_df = load_and_transform_data(file_lex, "LEX")
    pop_df = load_and_transform_data(file_pop, "POP")
    

    # Check if any files failed to load
    if gni_df is None or lex_df is None or pop_df is None:
        st.error("Data loading failed. Please check the file paths and try again.")
        return None  

    try:
        # Merge DataFrames after fill NaN
        merged_df = lex_df.merge(gni_df, on=['country', 'year']).merge(pop_df, on=['country', 'year'])
        # Convert year column to int
        merged_df["year"] = pd.to_numeric(merged_df["year"])
        def convert_notation(value):
            if isinstance(value, str):
                if value[-1].lower() == 'k':
                    return float(value[:-1]) * 1000
                elif value[-1].lower() == 'm':
                    return float(value[:-1]) * 1000000
                elif value[-1].lower() == 'b':
                    return float(value[:-1]) * 1000000000
            return value  # Return unchanged if not applicable

        columns_to_convert = ['GNI', 'POP']  # Add column names you want to convert
        for col in columns_to_convert:
            merged_df[col] = merged_df[col].apply(convert_notation).astype(float)
        
        return merged_df
    
    except Exception as e:  # Catching a broader range of potential errors during the merge
        print(f"Error merging DataFrames: {e}")
        st.error("An error occurred while merging the data. Please check the logs for details.")
        return None
    
    



# ----------------------
# Streamlit App
# ----------------------
merged_df = load_and_transform_df()
merged_df['GNI_log'] = merged_df['GNI'].apply(np.log)
# Add Year Slider (after converting to numeric)
year_min = int(merged_df['year'].min())
year_max = int(merged_df['year'].max())
selected_year = st.slider("Year", year_min, year_max, year_max)

all_countries = sorted(merged_df['country'].unique())
def_countries = ["Japan", "China", "Colombia", "USA", "Germany"]
selected_countries = st.multiselect("Countries", all_countries, default=def_countries)

# Filter Data based on year and selected countries
filtered_df = merged_df[
    (merged_df['year'] == selected_year) & (merged_df['country'].isin(selected_countries))
]

# Determine the maximum GNI value across all years to keep the x-axis fixed
max_gni = merged_df["GNI"].max()
max_lex = merged_df["LEX"].max()
min_pop = filtered_df['POP'].min()
max_pop = filtered_df['POP'].max()
mean_pop = filtered_df['POP'].mean()


# ----------------------
# Streamlit Visualization
# ----------------------

# Create the scatter plot with Plotly Express
fig = px.scatter(
    filtered_df, 
    x="GNI", 
    y="LEX", 
    size="POP", 
    color="country",
    log_x=True,
    size_max=50,
    title="Relationship Between GNI per Capita and Life Expectancy<br>(Bubble Size Represents Population)",
    hover_name="country",
    hover_data={"POP":":,.0f"}  
)

# Customize appearance
fig.update_traces(
    marker=dict(line=dict(width=0.5, color="DarkSlateGrey"))
)

# Adjust axis ranges for better visual clarity
fig.update_layout(
    yaxis=dict(range=[0, filtered_df["LEX"].max() * 1.1]), 
    xaxis=dict(range=[0, np.log10(max_gni) + 0.2])
)
st.plotly_chart(fig)

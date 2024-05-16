import streamlit as st
import pandas as pd
import plotly.express as px


st.title('Gapminder')
st.write("Unlocking Lifetimes: Visualizing Progress in Longevity and Poverty Eradication")

# ----------------------
# Data Loading & Preprocessing
# ----------------------

def load_and_transform_df():
    """Loads all CSVs, processes them, and returns the merged DataFrame."""

    def load_and_transform_data(file_path, value_name):
        """Loads a CSV file, melts it, and standardizes relevant columns to numeric."""

        try:
            df = pd.read_csv(file_path)
            melted_df = pd.melt(df, id_vars=['country'], var_name='year', value_name=value_name)

            # Convert relevant columns to numeric (with fillna)
            for col in [value_name]:  # 'POP' is also included
                melted_df[col] = (
                    melted_df[col]
                    .astype(str)
                    .str.replace(r'[kMB]', '', regex=True)
                    .str.replace(',', '.', regex=False)  # For European decimals
                    .replace('', '0')  # Replace blanks with 0
                    .astype(float)
                )

                # Fill NaN with Forward Fill
                melted_df[col] = melted_df[col].fillna(method='ffill')

                # Scale values
                melted_df[col] = melted_df[col].apply(
                    lambda x: x * 1000 if x < 1000000 else (x * 1000000 if x < 1000000000 else x)
                )

            return melted_df

        except FileNotFoundError:
            print(f"Error: File not found at {file_path}")
            return None

    # Load and transform data
    gni_df = load_and_transform_data("/Users/ligiavergara/gapminder/app/gni.csv", "GNI")
    lex_df = load_and_transform_data("/Users/ligiavergara/gapminder/app/lex.csv", "LEX")
    pop_df = load_and_transform_data("/Users/ligiavergara/gapminder/app/pop.csv", "POP")

    # Check if any files failed to load
    if gni_df is None or lex_df is None or pop_df is None:
        st.error("Data loading failed. Please check the file paths and try again.")
        return None  

    try:
        # Merge DataFrames after fill NaN
        merged_df = gni_df.merge(lex_df, on=['country', 'year']).merge(pop_df, on=['country', 'year'])
        # Convert year column to int
        merged_df["year"] = pd.to_numeric(merged_df["year"])
        return merged_df
    
    except Exception as e:  # Catching a broader range of potential errors during the merge
        print(f"Error merging DataFrames: {e}")
        st.error("An error occurred while merging the data. Please check the logs for details.")
        return None



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
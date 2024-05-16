import pandas as pd

def load_and_transform_data(file_path, value_name):
    df = pd.read_csv(file_path)
    melted_df = pd.melt(df, id_vars=['country'], var_name='year', value_name=value_name)

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

# Save as Parquet
merged_df.to_parquet("app/gapminder_data.parquet")

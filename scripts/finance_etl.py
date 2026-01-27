import pandas as pd

# Load raw data
input_path = "../data/raw/finance_raw.csv" # Since this was inside script folder, we go back two levels to reach data folder => ../ 
output_path = "../data/processed/finance_clean.csv"

df = pd.read_csv(input_path)

# Standardize column names
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

# Handle missing values
df["growthrate"] = df["growthrate"].fillna(0)

# Create profit column
df["profit"] = df["revenue"] * (df["profitmargin"] / 100)

# Select relevant columns
df_clean = df[
    [
        "companyid",
        "companyname",
        "industry",
        "region",
        "year",
        "revenue",
        "profitmargin",
        "growthrate",
        "marketcap",
        "profit"
    ]
]

# Rename columns to snake_case consistency
df_clean = df_clean.rename(columns={
    "companyid": "company_id",
    "companyname": "company_name",
    "profitmargin": "profit_margin",
    "growthrate": "growth_rate",
    "marketcap": "market_cap"
})

# Save processed data
df_clean.to_csv(output_path, index=False)

print("Finance ETL completed successfully.")

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

# 1. Ensure profitmargin is numeric
df["profitmargin"] = pd.to_numeric(df["profitmargin"], errors="coerce")

# 2. If profitmargin looks like whole percentages (e.g. 553 = 5.53%)
# assume values above 100 are scaled incorrectly
df.loc[df["profitmargin"].abs() > 100, "profitmargin"] = (
    df.loc[df["profitmargin"].abs() > 100, "profitmargin"] / 100
)

# 3. Cap profit margin to realistic bounds
df["profitmargin"] = df["profitmargin"].clip(lower=-50, upper=50)

# 4. Recalculate profit (Revenue is already in millions)
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

print(df[["revenue", "profitmargin", "profit"]].describe())
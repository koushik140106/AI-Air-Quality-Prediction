import pandas as pd
import os

input_file = "merged_air_quality.csv"
output_file = "cleaned_air_quality.csv"

# Remove old cleaned file if exists
if os.path.exists(output_file):
    os.remove(output_file)

chunk_size = 50_000   # very safe for low RAM
first_chunk = True

# Exact column names to extract (raw data)
use_columns = [
    "PM2.5 (ug/m3)",
    "PM10 (ug/m3)",
    "NO (ug/m3)",
    "NO2 (ug/m3)",
    "SO2 (ug/m3)",
    "CO (mg/m3)"
]

for chunk in pd.read_csv(
    input_file,
    usecols=lambda c: c in use_columns,
    chunksize=chunk_size,
    engine="python"
):
    # Rename columns
    chunk.rename(columns={
        "PM2.5 (ug/m3)": "PM25",
        "PM10 (ug/m3)": "PM10",
        "NO (ug/m3)": "NO",
        "NO2 (ug/m3)": "NO2",
        "SO2 (ug/m3)": "SO2",
        "CO (mg/m3)": "CO"
    }, inplace=True)

    # Convert to numeric safely
    chunk = chunk.apply(pd.to_numeric, errors="coerce")

    # Drop rows without PM2.5 (target)
    chunk = chunk.dropna(subset=["PM25"])

    # Fill remaining missing values
    chunk = chunk.ffill().bfill()

    # Append cleaned chunk to output CSV
    chunk.to_csv(
        output_file,
        mode="a",
        index=False,
        header=first_chunk
    )

    first_chunk = False
    del chunk  # free memory

print("✅ Cleaned data saved successfully using streaming (low RAM safe)")

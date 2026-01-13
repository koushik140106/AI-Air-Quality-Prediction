import pandas as pd
import glob

folder = r"C:\AK  storage\AU college\3rd sem\Python\data"

csv_files = glob.glob(folder + r"\*.csv")

print("Total files found:", len(csv_files))

if len(csv_files) == 0:
    print("❌ No CSV files found. Path still incorrect.")
else:
    dfs = []
    for file in csv_files:
        print("Reading:", file)
        dfs.append(pd.read_csv(file))

    merged_df = pd.concat(dfs, ignore_index=True)
    merged_df.to_csv("merged_air_quality.csv", index=False)
    print("✅ merged_air_quality.csv created")

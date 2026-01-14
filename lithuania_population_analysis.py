
# ================================================================
# Lithuania Population Decline Analysis (1990–2024)
# Student: Milad Seifi
# ================================================================

import pandas as pd
import matplotlib.pyplot as plt
from google.colab import files

plt.rcParams["figure.figsize"] = (10, 6)
plt.rcParams["axes.grid"] = True

print("Please upload your Eurostat CSV file (SDMX-CSV format).")
uploaded = files.upload()

csv_path = list(uploaded.keys())[0]
print("File loaded:", csv_path)

def load_lithuania_population(csv_path: str) -> pd.DataFrame:
    df = pd.read_csv(csv_path)

    rename_map = {
        "TIME_PERIOD": "year",
        "OBS_VALUE": "population",
        "geo": "geo",
        "sex": "sex",
        "age": "age",
    }
    df = df.rename(columns=rename_map)

    df["year"] = pd.to_numeric(df["year"], errors="coerce")
    df = df.dropna(subset=["year"])
    df["year"] = df["year"].astype(int)

    df["population"] = pd.to_numeric(df["population"], errors="coerce")

    df_lt = df[
        (df["geo"].isin(["LT", "Lithuania"])) &
        (df["sex"].isin(["T", "Total"])) &
        (df["age"].isin(["TOTAL", "Total"]))
    ].copy()

    df_lt = df_lt[(df_lt["year"] >= 1990) & (df_lt["year"] <= 2024)]
    df_lt = df_lt[["year", "population"]].dropna()

    return df_lt.sort_values("year").reset_index(drop=True)

df = load_lithuania_population(csv_path)
display(df.head())
display(df.tail())

def add_change_columns(df):
    df = df.copy()
    df["abs_change"] = df["population"].diff()
    df["pct_change"] = df["population"].pct_change() * 100
    return df

df = add_change_columns(df)

total_change = df["population"].iloc[-1] - df["population"].iloc[0]
avg_pct_change = df["pct_change"].mean()
worst_year = df.loc[df["abs_change"].idxmin(), "year"]
worst_value = df["abs_change"].min()

print("======================================")
print("SUMMARY STATISTICS (1990–2024)")
print("======================================")
print(f"Total population change: {total_change:,.0f} people")
print(f"Average yearly % change: {avg_pct_change:.3f}%")
print(f"Worst year of population loss: {worst_year} ({worst_value:,.0f} people)")
print("======================================")

def plot_population_trend(df):
    plt.figure()
    plt.plot(df["year"], df["population"], marker="o")
    plt.title("Population of Lithuania (1990–2024)")
    plt.xlabel("Year")
    plt.ylabel("Population")
    plt.tight_layout()
    plt.savefig("lt_population_trend.png", dpi=150)
    plt.show()

def plot_abs_change(df):
    plt.figure()
    plt.bar(df["year"], df["abs_change"])
    plt.title("Yearly Absolute Population Change")
    plt.xlabel("Year")
    plt.ylabel("Change in Population")
    plt.axhline(0, color="black")
    plt.tight_layout()
    plt.savefig("lt_population_abs_change.png", dpi=150)
    plt.show()

def plot_pct_change(df):
    plt.figure()
    plt.bar(df["year"], df["pct_change"])
    plt.title("Yearly % Population Change")
    plt.xlabel("Year")
    plt.ylabel("Percent Change (%)")
    plt.axhline(0, color="black")
    plt.tight_layout()
    plt.savefig("lt_population_pct_change.png", dpi=150)
    plt.show()

plot_population_trend(df)
plot_abs_change(df)
plot_pct_change(df)

print("All figures saved.")

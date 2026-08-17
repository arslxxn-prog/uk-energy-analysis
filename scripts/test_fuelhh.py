import requests
import pandas as pd


URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

params = {
    "settlementDateFrom": "2025-01-01",
    "settlementDateTo": "2025-01-02",
    "format": "json",
}


def main():
    response = requests.get(URL, params=params, timeout=60)

    print("Request URL:")
    print(response.url)
    print()

    print("HTTP status:")
    print(response.status_code)
    print()

    response.raise_for_status()

    payload = response.json()

    df = pd.DataFrame(payload["data"])

    print("Columns:")
    print(df.columns.tolist())
    print()

    print("Number of records:")
    print(len(df))
    print()

    print("First 10 records:")
    print(df.head(10).to_string(index=False))
    print()

    print("Fuel types:")
    print(sorted(df["fuelType"].unique()))

    print("\nSettlement dates:")
    print(sorted(df["settlementDate"].unique()))

    print("\nNumber of settlement periods:")
    print(df["settlementPeriod"].nunique())

    print("\nRecords by fuel type:")
    print(
        df["fuelType"]
        .value_counts()
        .sort_index()
)

    print("\nGeneration summary:")
    print(df["generation"].describe())

if __name__ == "__main__":
    main()
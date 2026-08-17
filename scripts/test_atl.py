import requests
import pandas as pd


URL = "https://data.elexon.co.uk/bmrs/api/v1/demand/actual/total"

params = {
    "from": "2025-01-01",
    "to": "2025-01-02",
    "format": "json",
}


def main():
    response = requests.get(
        URL,
        params=params,
        timeout=60,
    )

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

    print("Settlement periods:")
    print(sorted(df["settlementPeriod"].unique()))


if __name__ == "__main__":
    main()
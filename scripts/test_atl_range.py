import requests
import pandas as pd

URL = "https://data.elexon.co.uk/bmrs/api/v1/demand/actual/total"

params = {
    "from": "2025-01-01T00:00:00Z",
    "to": "2025-01-08T00:00:00Z",
    "format": "json",
}

response = requests.get(
    URL,
    params=params,
    timeout=60
)

print("Status:", response.status_code)

response.raise_for_status()

payload = response.json()

df = pd.DataFrame(payload["data"])

print("Rows:", len(df))
print("Unique timestamps:", df["startTime"].nunique())
print("Minimum startTime:", df["startTime"].min())
print("Maximum startTime:", df["startTime"].max())

print("\nFirst 10 rows:")
print(df.head(10).to_string(index=False))

print("\nSettlement periods:")
print(sorted(df["settlementPeriod"].unique()))
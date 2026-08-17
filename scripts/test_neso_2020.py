import requests
import pandas as pd

RESOURCE_ID = "33ba6857-2a55-479f-9308-e5c4c53d4381"

URL = "https://api.neso.energy/api/3/action/datastore_search"

params = {
    "resource_id": RESOURCE_ID,
    "limit": 5,
}

response = requests.get(
    URL,
    params=params,
    timeout=60,
)

print("Status:", response.status_code)

response.raise_for_status()

payload = response.json()

print("\nTotal records available:")
print(payload["result"]["total"])

df = pd.DataFrame(
    payload["result"]["records"]
)

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 records:")
print(df.to_string(index=False))
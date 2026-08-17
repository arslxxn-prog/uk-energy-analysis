import requests

PACKAGE_URL = (
    "https://api.neso.energy/api/3/action/"
    "datapackage_show"
)

params = {
    "id": "historic-demand-data"
}

response = requests.get(
    PACKAGE_URL,
    params=params,
    timeout=60
)

response.raise_for_status()

payload = response.json()
resources = payload["result"]["resources"]

print(f"Resources found: {len(resources)}\n")

for resource in resources:
    name = resource.get("name", "")
    resource_id = resource.get("id", "")

    if "historic_demand_data_" in name.lower():
        print(f"NAME: {name}")
        print(f"ID:   {resource_id}")
        print("-" * 70)
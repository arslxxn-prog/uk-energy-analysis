from pathlib import Path
import time

import pandas as pd
import requests


BASE_URL = "https://api.neso.energy/api/3/action/datastore_search"

RESOURCES = {
    2020: "33ba6857-2a55-479f-9308-e5c4c53d4381",
    2021: "18c69c42-f20d-46f0-84e9-e279045befc6",
    2022: "bb44a1b5-75b1-4db2-8491-257f23385006",
    2023: "bf5ab335-9b40-4ea4-b93a-ab4af7bce003",
    2024: "f6d02c0f-957b-48cb-82ee-09003f2ba759",
    2025: "b2bde559-3455-4021-b179-dfe60c0337b0",
}

OUTPUT_DIR = Path("data/raw/neso_demand")

PAGE_SIZE = 5000
REQUEST_TIMEOUT = 60
SLEEP_BETWEEN_REQUESTS = 0.2


def fetch_resource(resource_id: str) -> pd.DataFrame:
    """Download an entire NESO DataStore resource using pagination."""

    records = []
    offset = 0

    while True:

        params = {
            "resource_id": resource_id,
            "limit": PAGE_SIZE,
            "offset": offset,
        }

        response = requests.get(
            BASE_URL,
            params=params,
            timeout=REQUEST_TIMEOUT,
        )

        response.raise_for_status()

        payload = response.json()

        result = payload["result"]

        batch = result["records"]

        if not batch:
            break

        records.extend(batch)

        print(
            f"Downloaded {len(records):,} "
            f"of {result['total']:,}"
        )

        offset += len(batch)

        if offset >= result["total"]:
            break

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    return pd.DataFrame(records)


def download_year(year: int, resource_id: str) -> None:

    OUTPUT_DIR.mkdir(
        parents=True,
        exist_ok=True
    )

    output_path = (
        OUTPUT_DIR / f"neso_demand_{year}.csv"
    )

    if output_path.exists():
        print("=" * 70)
        print(f"Skipping {year}")
        print(f"File already exists: {output_path}")
        print("=" * 70)
        return

    print("=" * 70)
    print(f"Downloading NESO demand {year}")
    print("=" * 70)

    df = fetch_resource(resource_id)

    print(
        f"\nRecords downloaded: "
        f"{len(df):,}"
    )

    print(
        f"Columns: "
        f"{df.columns.tolist()}"
    )

    df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Saved to: {output_path}"
    )


def main():

    for year, resource_id in RESOURCES.items():

        download_year(
            year,
            resource_id
        )

        time.sleep(
            SLEEP_BETWEEN_REQUESTS
        )


if __name__ == "__main__":
    main()
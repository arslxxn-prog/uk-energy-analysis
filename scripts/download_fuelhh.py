from datetime import date, timedelta
from pathlib import Path
import time

import pandas as pd
import requests


BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/datasets/FUELHH"

START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 12, 31)

OUTPUT_DIR = Path("data/raw/fuelhh")

CHUNK_DAYS = 7
REQUEST_TIMEOUT = 60
RETRY_ATTEMPTS = 3
SLEEP_BETWEEN_REQUESTS = 0.5


def fetch_fuelhh(start_date: date, end_date: date) -> pd.DataFrame:
    """Download one inclusive settlement-date chunk."""

    params = {
        "settlementDateFrom": start_date.isoformat(),
        "settlementDateTo": end_date.isoformat(),
        "format": "json",
    }

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=REQUEST_TIMEOUT,
            )

            response.raise_for_status()

            payload = response.json()

            if "data" not in payload:
                raise ValueError("API response does not contain 'data'.")

            return pd.DataFrame(payload["data"])

        except (requests.RequestException, ValueError) as error:
            print(
                f"Request failed: "
                f"{start_date} -> {end_date} "
                f"(attempt {attempt}/{RETRY_ATTEMPTS})"
            )
            print(error)

            if attempt == RETRY_ATTEMPTS:
                raise

            time.sleep(2 * attempt)

    raise RuntimeError("Unexpected downloader state.")


def download_year(start_date: date, end_date: date) -> None:
    """Download an entire period in smaller chunks."""

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    output_path = (
        OUTPUT_DIR
        / f"fuelhh_{start_date.year}.csv"
    )

    if output_path.exists():
        print("=" * 70)
        print(f"Skipping {start_date.year}")
        print(f"File already exists: {output_path}")
        print("=" * 70)
        return

    chunks = []
    current_start = start_date

    total_chunks = (
        (end_date - start_date).days // CHUNK_DAYS
    ) + 1

    chunk_number = 0

    while current_start <= end_date:

        current_end = min(
            current_start + timedelta(days=CHUNK_DAYS - 1),
            end_date,
        )

        chunk_number += 1

        print(
            f"\n[{chunk_number}/{total_chunks}] "
            f"{current_start} -> {current_end}"
        )

        df_chunk = fetch_fuelhh(
            current_start,
            current_end,
        )

        if not df_chunk.empty:
            chunks.append(df_chunk)

            print(
                f"Rows returned: {len(df_chunk):,}"
            )
        else:
            print("No data returned.")

        current_start = current_end + timedelta(days=1)

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    if not chunks:
        raise RuntimeError("No data was downloaded.")

    df = pd.concat(
        chunks,
        ignore_index=True,
    )

    # Remove accidental duplicate records across chunk boundaries.
    df = df.drop_duplicates()

    output_path = (
        OUTPUT_DIR
        / f"fuelhh_{start_date.year}.csv"
    )

    df.to_csv(
        output_path,
        index=False,
    )

    print("\n" + "=" * 70)
    print("DOWNLOAD COMPLETE")
    print("=" * 70)

    print(f"Records: {len(df):,}")

    print(
        f"Settlement dates: "
        f"{df['settlementDate'].min()} "
        f"-> "
        f"{df['settlementDate'].max()}"
    )

    print(
        f"Fuel categories: "
        f"{df['fuelType'].nunique()}"
    )

    print(f"Saved to: {output_path}")


def main() -> None:
    for year in range(START_DATE.year, END_DATE.year + 1):

        year_start = date(year, 1, 1)
        year_end = date(year, 12, 31)

        # Respect the overall start/end boundaries
        year_start = max(year_start, START_DATE)
        year_end = min(year_end, END_DATE)

        download_year(
            year_start,
            year_end
        )

        time.sleep(SLEEP_BETWEEN_REQUESTS)


if __name__ == "__main__":
    main()
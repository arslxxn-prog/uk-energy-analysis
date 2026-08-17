
from datetime import date, timedelta
from pathlib import Path
import time

import pandas as pd
import requests


BASE_URL = "https://data.elexon.co.uk/bmrs/api/v1/demand/actual/total"

START_DATE = date(2020, 1, 1)
END_DATE = date(2025, 12, 31)

OUTPUT_DIR = Path("data/raw/atl")

CHUNK_DAYS = 7
REQUEST_TIMEOUT = 60
RETRY_ATTEMPTS = 3
SLEEP_BETWEEN_REQUESTS = 0.5


def fetch_atl(start_date: date, end_date: date) -> pd.DataFrame:
    """Download one ATL date-range chunk."""

    params = {
        "from": f"{start_date.isoformat()}T00:00:00Z",
        "to": f"{end_date.isoformat()}T00:00:00Z",
        "format": "json",
    }

    for attempt in range(1, RETRY_ATTEMPTS + 1):
        try:
            response = requests.get(
                BASE_URL,
                params=params,
                timeout=60,
            )

            response.raise_for_status()

            payload = response.json()

            if "data" not in payload:
                raise ValueError(
                    "API response does not contain a 'data' field."
                )

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


def download_year(year: int) -> None:
    """Download one complete calendar year in 7-day chunks."""

    output_path = OUTPUT_DIR / f"atl_{year}.csv"

    if output_path.exists():
        print("=" * 70)
        print(f"Skipping {year}")
        print(f"File already exists: {output_path}")
        print("=" * 70)
        return

    year_start = max(
        date(year, 1, 1),
        START_DATE
    )

    year_end = min(
        date(year, 12, 31),
        END_DATE
    )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    chunks = []
    current_start = year_start

    total_chunks = (
        (year_end - year_start).days // CHUNK_DAYS
    ) + 1

    chunk_number = 0

    print("=" * 70)
    print(f"Downloading ATL {year}")
    print("=" * 70)

    while current_start <= year_end:

        current_end = min(
            current_start + timedelta(days=CHUNK_DAYS),
            year_end + timedelta(days=1),
        )

        chunk_number += 1

        print(
            f"[{chunk_number}/{total_chunks}] "
            f"{current_start} -> {current_end}"
        )

        df_chunk = fetch_atl(
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

        current_start = current_end

        time.sleep(SLEEP_BETWEEN_REQUESTS)

    if not chunks:
        raise RuntimeError(
            f"No ATL data downloaded for {year}."
        )

    df = pd.concat(
        chunks,
        ignore_index=True,
    )

    df = df.drop_duplicates()

    df.to_csv(
        output_path,
        index=False,
    )

    print()
    print(f"Records: {len(df):,}")
    print(
        f"Settlement dates: "
        f"{df['settlementDate'].min()} "
        f"-> "
        f"{df['settlementDate'].max()}"
    )
    print(
        f"Unique start times: "
        f"{df['startTime'].nunique():,}"
    )
    print(f"Saved to: {output_path}")
    print()


def main() -> None:
    for year in range(
        START_DATE.year,
        END_DATE.year + 1
    ):
        download_year(year)
        time.sleep(SLEEP_BETWEEN_REQUESTS)


if __name__ == "__main__":
    main()
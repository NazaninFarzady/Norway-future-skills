import json
import time
from pathlib import Path

import requests


API_URL = (
    "https://arbeidsplassen.nav.no/"
    "stillinger/api/search"
)

OUTPUT_FILE = Path(
    "data/raw/all_jobs.json"
)

BATCH_SIZE = 100
MAX_JOBS = 10_000
REQUEST_DELAY = 0.5
TIMEOUT = 30


# ---------------------------------------------------------
# Collect job postings
# ---------------------------------------------------------

all_jobs = []
seen_job_ids = set()

start = 0


while len(all_jobs) < MAX_JOBS:

    params = {
        "from": start,
        "size": BATCH_SIZE
    }

    try:
        response = requests.get(
            API_URL,
            params=params,
            timeout=TIMEOUT
        )

        response.raise_for_status()

        data = response.json()

    except requests.RequestException as error:
        print(
            "Request failed:",
            error
        )
        break

    except ValueError:
        print(
            "Response was not valid JSON."
        )
        break


    hits = (
        data
        .get("hits", {})
        .get("hits", [])
    )


    if not hits:
        print(
            "No more jobs found."
        )
        break


    # Avoid accidental duplicate postings
    for job in hits:

        source = job.get(
            "_source",
            {}
        )

        job_id = source.get(
            "uuid"
        )

        if (
            job_id
            and job_id in seen_job_ids
        ):
            continue

        if job_id:
            seen_job_ids.add(
                job_id
            )

        all_jobs.append(
            job
        )

        if (
            len(all_jobs)
            >= MAX_JOBS
        ):
            break


    print(
        f"Downloaded "
        f"{len(all_jobs):,} jobs"
    )


    start += BATCH_SIZE

    time.sleep(
        REQUEST_DELAY
    )


# ---------------------------------------------------------
# Save raw data
# ---------------------------------------------------------

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

with OUTPUT_FILE.open(
    "w",
    encoding="utf-8"
) as file:

    json.dump(
        all_jobs,
        file,
        ensure_ascii=False,
        indent=2
    )


print(
    "\\nCollection completed."
)

print(
    "Total jobs saved:",
    f"{len(all_jobs):,}"
)

print(
    "Output file:",
    OUTPUT_FILE
)
import requests
import json
import time

API_URL = "https://arbeidsplassen.nav.no/stillinger/api/search"

all_jobs = []

start = 0
batch_size = 100

while True:
    params = {
        "from": start,
        "size": batch_size
    }

    response = requests.get(API_URL, params=params)
    data = response.json()

    if "hits" not in data:
        print("No more jobs or unexpected response:")
        print(data)
        break

    jobs = data["hits"]["hits"]

    if not jobs:
        break

    all_jobs.extend(jobs)

    print(f"Downloaded {len(all_jobs)} jobs")

    start += batch_size

    time.sleep(0.5)


with open("data/raw/all_jobs.json", "w", encoding="utf-8") as file:
    json.dump(all_jobs, file, ensure_ascii=False, indent=2)

print("Finished!")
print("Total jobs saved:", len(all_jobs))
import json
from pathlib import Path

import pandas as pd


INPUT_FILE = Path("data/raw/all_jobs.json")
OUTPUT_FILE = Path("data/processed/jobs_clean.csv")


# ---------------------------------------------------------
# Load raw job postings
# ---------------------------------------------------------

with INPUT_FILE.open(
    "r",
    encoding="utf-8"
) as file:
    jobs = json.load(file)


# ---------------------------------------------------------
# Helper functions
# ---------------------------------------------------------

def first_city(source):
    locations = source.get("locationList") or []

    for location in locations:
        city = location.get("city")

        if city:
            return city.strip()

    return None


def join_names(items):
    items = items or []

    names = [
        item.get("name", "").strip()
        for item in items
        if item.get("name", "").strip()
    ]

    return ", ".join(names)


def join_skills(source):
    properties = source.get("properties") or {}

    skills = properties.get("searchtagsai") or []

    skills = [
        str(skill).strip()
        for skill in skills
        if str(skill).strip()
    ]

    return ", ".join(skills)


# ---------------------------------------------------------
# Clean jobs
# ---------------------------------------------------------

clean_jobs = []

for job in jobs:

    source = job.get("_source", {})

    city = first_city(source)

    occupation = join_names(
        source.get("occupationList")
    )

    category = join_names(
        source.get("categoryList")
    )

    skills = join_skills(source)

    clean_jobs.append({
        "job_id": source.get("uuid"),
        "title": source.get("title"),
        "company": source.get("businessName"),
        "published": source.get("published"),
        "expires": source.get("expires"),

        "city":
            city
            if city
            else "Missing location",

        "occupation":
            occupation
            if occupation
            else "Not classified",

        "category":
            category
            if category
            else "Not classified",

        "skills":
            skills
            if skills
            else "No skills listed",

        "has_city": bool(city),
        "has_occupation": bool(occupation),
        "has_skills": bool(skills)
    })


# ---------------------------------------------------------
# Save cleaned dataset
# ---------------------------------------------------------

df = pd.DataFrame(clean_jobs)

OUTPUT_FILE.parent.mkdir(
    parents=True,
    exist_ok=True
)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


print("Cleaning completed")
print("Rows:", len(df))
print("Columns:", list(df.columns))
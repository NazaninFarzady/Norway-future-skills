import json
import pandas as pd


INPUT_FILE = "data/raw/all_jobs.json"
OUTPUT_FILE = "data/processed/jobs_clean.csv"


with open(INPUT_FILE, "r", encoding="utf-8") as file:
    jobs = json.load(file)


clean_jobs = []

for job in jobs:
    source = job["_source"]

    city = source.get("locationList", [{}])[0].get("city")

    occupation = ", ".join(
        [
            item.get("name", "")
            for item in source.get("occupationList", [])
        ]
    )

    category = ", ".join(
        [
            item.get("name", "")
            for item in source.get("categoryList", [])
        ]
    )

    skills = ", ".join(
        source.get("properties", {}).get("searchtagsai", [])
    )


    clean_jobs.append({
        "job_id": source.get("uuid"),
        "title": source.get("title"),
        "company": source.get("businessName"),
        "published": source.get("published"),
        "expires": source.get("expires"),

        "city": city if city else "Unknown",

        "occupation": occupation if occupation else "Not classified",

        "category": category if category else "Not classified",

        "skills": skills if skills else "No skills listed",

        "has_city": bool(city),
        "has_occupation": bool(occupation),
        "has_skills": bool(skills)
    })


df = pd.DataFrame(clean_jobs)

df.to_csv(
    OUTPUT_FILE,
    index=False,
    encoding="utf-8"
)


print("Cleaning completed")
print("Rows:", len(df))
print("Columns:", list(df.columns))
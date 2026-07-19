import requests
import json
from loguru import logger 

URL = "https://public.zwayam.com/jobs/search"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}


def fetch_jobs(search_term = "python developer" , location = "India"):
    pagination_start = 0
    all_jobs=[]

    while True:
        payload = {
            "filterCri": json.dumps({
                "paginationStartNo": pagination_start,
                "selectedCall": "sort",
                "sortCriteria": {
                    "name": "modifiedDate",
                    "isAscending": False
                },
                "anyOfTheseWords": search_term,
                "facetSelectionString": {
                    "Location": [
                        location
                    ]
                }
            }),
            "domain": "careers.persistent.com",
            "companyId": "MTYzNDQ="
        }

        try:
            response = requests.post(URL , headers = HEADERS , data= payload , timeout = 30)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:

            logger.error(f"Request failed: {e}")

            break

        try:
            response_json = response.json()

            jobs = response_json["data"]["data"]
        except KeyError:

            logger.error("Unexpected API response.")

            break

        if not jobs:
            logger.info("No more Jobs found")
            break
        logger.info(f"Received {len(jobs)} jobs")
        
        for job in jobs:
            source = job["_source"]

            job_data = {
                "title": source.get("jobTitle"),
                "company": "Persistent",
                "experience": source.get("experienceUIField"),
                "reference_number": source.get("referenceNumber"),
                "job_code": source.get("jobCode"),
                "skills": source.get("desiredSkillList", [])
            }

            locations = source.get("jobLocationRecord", [])

            job_data["locations"] = [
            loc.get("formattedLocation")
            for loc in locations
            ]

            all_jobs.append(job_data)

        pagination_start += len(jobs)

        logger.info(f"Downloaded {len(all_jobs)} jobs...")

    with open(
        "scraped_data/persistent.json",
        "w",
        encoding="utf-8"
    ) as file:

        json.dump(
            all_jobs,
            file,
            indent=4,
            ensure_ascii=False
        )

        logger.success(f"Finished! Saved {len(all_jobs)} jobs.")


if __name__ == "__main__":
    fetch_jobs()
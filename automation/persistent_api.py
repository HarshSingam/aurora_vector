import json
import os
import requests
from loguru import logger

from app.db_connection import SessionLocal
from app.models import User

URL = "https://public.zwayam.com/jobs/search"
HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Content-Type": "application/x-www-form-urlencoded"
}
PERSISTENT_FILE = "scraped_data/persistent.json"


def load_existing_jobs(path=PERSISTENT_FILE):
    if not os.path.exists(path):
        return []

    try:
        with open(path, encoding="utf-8") as file:
            return json.load(file)
    except (json.JSONDecodeError, OSError) as exc:
        logger.warning(f"Could not read existing jobs from {path}: {exc}")
        return []


def save_jobs_to_json(jobs, path=PERSISTENT_FILE):
    os.makedirs(os.path.dirname(path), exist_ok=True)

    with open(path, "w", encoding="utf-8") as file:
        json.dump(jobs, file, indent=4, ensure_ascii=False)


def dedupe_jobs(jobs):
    unique_jobs = {}

    for job in jobs:
        job_code = job.get("job_code")
        if job_code:
            key = job_code
        else:
            key = (
                f"{job.get('company')}|{job.get('title')}|{job.get('location')}|{job.get('salary')}"
            )

        if key not in unique_jobs:
            unique_jobs[key] = job

    return list(unique_jobs.values())


def fetch_jobs(search_term, search_location, company, company_id, domain):
    pagination_start = 0
    all_jobs=[]

    # logger.info(f"Search Term : {search_term}")
    # logger.info(f"Location    : {location}")
    # logger.info(f"Company ID  : {company_id}")
    # logger.info(f"Domain      : {domain}")

    while True:
        payload = {
            "filterCri": json.dumps({
                "paginationStartNo": pagination_start,
                "selectedCall": "search",
                "sortCriteria": {
                    "name": "modifiedDate",
                    "isAscending": False
                },
                "anyOfTheseWords": search_term,
                "facetSelectionString": {
                    "Location": [
                        search_location
                    ]
                }
            }),
            "domain": domain,
            "companyId": company_id
        }

        try:
            logger.info(f"Requesting page starting at {pagination_start} for role '{search_term}'")
            response = requests.post(URL, headers=HEADERS, data=payload, timeout=30)
            response.raise_for_status()
        except requests.exceptions.RequestException as exc:
            logger.error(f"Request failed for '{search_term}': {exc}")
            break

        try:
            response_json = response.json()
            data = response_json.get("data")

            if data is None:
                logger.warning(f"No data returned for search term: '{search_term}'")
                break

            jobs = data.get("data", [])
        except (ValueError, KeyError) as exc:
            logger.error(f"Unexpected API response for '{search_term}': {exc}")
            break

        if not jobs:
            logger.info(f"No more jobs found for '{search_term}'")
            break

        logger.info(f"Received {len(jobs)} jobs for '{search_term}'")

        for job in jobs:
            source = job.get("_source", {})
            locations = source.get("jobLocationRecord", [])
            location_text = ", ".join(
                loc.get("formattedLocation")
                for loc in locations
                if loc.get("formattedLocation")
            )

            min_salary = source.get("minJobSalary")
            max_salary = source.get("maxJobSalary")

            if min_salary and max_salary:
                salary = f"{min_salary} - {max_salary}"
            elif min_salary:
                salary = min_salary
            elif max_salary:
                salary = max_salary
            else:
                salary = "Not Disclosed"

            job_data = {
                "job_code": source.get("jobCode"),
                "company": company,
                "title": source.get("jobTitle"),
                "location": location_text,
                "salary": salary,
                "skills": source.get("desiredSkillList", []),
                "search_term": search_term.strip()
            }

            all_jobs.append(job_data)

        pagination_start += len(jobs)
        logger.info(f"Downloaded {len(all_jobs)} jobs for '{search_term}' so far")

    return all_jobs

if __name__ == "__main__":

    db = SessionLocal()

    users = db.query(User).all()

    existing_jobs = load_existing_jobs()
    all_jobs = list(existing_jobs)

    COMPANY = "Persistent"
    COMPANY_ID = "MTYzNDQ="
    DOMAIN = "careers.persistent.com"

    for user in users:

        logger.info(f"Processing user: {user.name}")

        roles = [role.strip() for role in user.search_terms.split(",") if role.strip()]

        for role in roles:

            logger.info(f"Searching for: {role}")

            jobs = fetch_jobs(

                search_term=role,

                search_location=user.location,

                company=COMPANY,

                company_id=COMPANY_ID,

                domain=DOMAIN

            )

            all_jobs.extend(jobs)

    all_jobs = dedupe_jobs(all_jobs)
    for job in all_jobs:
        job.pop("job_code", None)

    save_jobs_to_json(all_jobs)
    logger.success(f"Saved {len(all_jobs)} unique jobs to {PERSISTENT_FILE}")

    db.close()
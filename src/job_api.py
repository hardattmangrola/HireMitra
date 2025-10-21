from apify_client import ApifyClient
import os
import dotenv
from dotenv import load_dotenv
load_dotenv()
APIFY_API_KEY = os.getenv("APIFY_API_TOKEN")

if APIFY_API_KEY is None:
    raise ValueError("APIFY_API_KEY environment variable is not set. Please create a .env file with your Apify API key.")

apify_client = ApifyClient(APIFY_API_KEY)

def fetch_linkedin_jobs(search_query,location="india",rows=5):
    run_input={
        "title":search_query,
        "location":location,
        "rows":rows,
        "proxy":{
            "useApifyProxy": True,
            "apifyProxyGroups": ["RESIDENTIAL"]
        }
    }
    run = apify_client.actor("BHzefUZlZRKWxkTck").call(run_input=run_input)
    jobs=list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs[:5]  # Ensure we only return top 5


def fetch_naukri_jobs(search_query,location="india",rows=5):
    run_input = {
    "keyword": search_query,
    "location": location,
    "maxJobs": rows,
    "freshness":"all",
    "sortBy":"relevance",
    "experience":"all",
    }
    run = apify_client.actor("wsrn5gy5C4EDeYCcD").call(run_input=run_input)
    jobs=list(apify_client.dataset(run["defaultDatasetId"]).iterate_items())
    return jobs[:5]  # Ensure we only return top 5
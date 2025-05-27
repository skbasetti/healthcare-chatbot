import os
from google.cloud import bigquery

project_id = os.getenv("GOOGLE_CLOUD_PROJECT", "astral-outpost-460600-p3")
client = bigquery.Client(project=project_id)

def run_bq_query(query: str):
    try:
        query_job = client.query(query)
        return list(query_job.result())
    except Exception as e:
        print(f"BigQuery query failed: {e}")
        return []
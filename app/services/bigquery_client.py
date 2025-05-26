from google.cloud import bigquery

client = bigquery.Client()

def run_bq_query(query: str):
    query_job = client.query(query)
    return list(query_job.result())

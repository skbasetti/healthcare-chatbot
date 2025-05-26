from fastapi import APIRouter
from services.bigquery_client import run_bq_query

router = APIRouter()

@router.get("/benefits")
def get_benefits(patient_id: str):
    query = f"""
        SELECT START_YEAR, END_YEAR, PAYER, OWNERSHIP
        FROM `astral-outpost-460600-p3.Claims_queries_demo.benefits`
        WHERE PATIENT = '{patient_id}'
        ORDER BY START_YEAR DESC
        LIMIT 1
    """
    rows = run_bq_query(query)
    if not rows:
        return {"message": "No benefit data found."}
    row = rows[0]
    return {
        "start_year": row["START_YEAR"],
        "end_year": row["END_YEAR"],
        "payer": row["PAYER"],
        "ownership": row["OWNERSHIP"]
    }

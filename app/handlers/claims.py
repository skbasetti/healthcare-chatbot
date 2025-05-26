from fastapi import APIRouter, Query
from services.bigquery_client import run_bq_query

router = APIRouter()

@router.get("/claim-history")
def claim_history(patient_id: str):
    query = f"""
        SELECT
          p.FIRST AS first_name,
          p.LAST AS last_name,
          e.START AS visit_start,
          e.DESCRIPTION AS service_description,
          e.TOTAL_CLAIM_COST,
          e.PAYER_COVERAGE,
          pt.OWNERSHIP AS plan_ownership
        FROM
          `astral-outpost-460600-p3.Claims_queries_demo.patients` p
        JOIN
          `astral-outpost-460600-p3.Claims_queries_demo.encounters` e
        ON p.id = e.PATIENT
        LEFT JOIN
          `astral-outpost-460600-p3.Claims_queries_demo.benefits` pt
        ON p.id = pt.PATIENT
        WHERE p.id = '{patient_id}'
        ORDER BY e.START DESC
        LIMIT 5
    """
    rows = run_bq_query(query)
    claims = [
        {
            "visit_start": row["visit_start"],
            "service": row["service_description"],
            "cost": float(row["TOTAL_CLAIM_COST"]),
            "covered": float(row["PAYER_COVERAGE"]),
            "plan": row["plan_ownership"]
        } for row in rows
    ]
    return {"patient_id": patient_id, "claims": claims}
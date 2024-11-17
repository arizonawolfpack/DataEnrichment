from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional, List, Dict
import random

app = FastAPI()

class DataEnrichmentRequest(BaseModel):
    email: Optional[str] = None
    domain: Optional[str] = None
    enrich_fields: Optional[List[str]] = None

class DataEnrichmentResponse(BaseModel):
    enriched_data: Dict[str, Dict] = {}
    prediction: Optional[Dict[str, float]] = None
    data_score: Optional[Dict[str, float]] = None

# Mock data for enrichment
mock_data_sources = {
    "demographics": {"age": 30, "location": "New York"},
    "social_profiles": {"twitter": "@sample_user"},
    "financial_data": {"revenue": 100000}
}

@app.post("/enrich", response_model=DataEnrichmentResponse)
async def enrich_data(request: DataEnrichmentRequest):
    if not request.email and not request.domain:
        raise HTTPException(status_code=400, detail="Email or domain is required.")
    enriched_data = {field: mock_data_sources.get(field, {}) for field in request.enrich_fields or []}
    prediction = {"lifetime_value": random.uniform(1000, 10000)}
    data_score = {field: random.uniform(0.7, 1.0) for field in enriched_data}
    return DataEnrichmentResponse(enriched_data=enriched_data, prediction=prediction, data_score=data_score)
from fastapi import APIRouter
from src.nlp_recommender.recommendation_engine import ThreatMitigationRecommender
import os
knowledge_base_path = os.path.join(os.path.dirname(__file__), "../../processed_data/cicids_mitigations_kb.json")

router = APIRouter()
recommender = ThreatMitigationRecommender(knowledge_base_path=knowledge_base_path)

@router.post("/recommend")
def recommend_threat_mitigation(threat: dict):
    """
    Takes threat info and returns a full NLP-generated mitigation report.
    """
    context = threat.get("context", None)
    recommendations = recommender.generate_recommendations(threat, context)
    report = recommender.generate_report(recommendations)
    return {"report": report}
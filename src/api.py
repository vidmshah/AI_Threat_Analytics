from fastapi import FastAPI
from src.nlp_recommender.api import router as nlp_router
from src.prediction import router as prediction_router
from src.nlp_recommender.report_generator import router as report_router

app = FastAPI(
    title="AI-Powered Threat Center",
    description="One-stop platform for threat classification, prediction, and mitigation recommendation",
    version="1.0.0"
)

# Mount routes
app.include_router(nlp_router, prefix="/nlp", tags=["NLP Recommendation"])
app.include_router(prediction_router, prefix="/predict", tags=["Threat Prediction"])
app.include_router(report_router, prefix="/report", tags=["Report Generation"])

@app.get("/")
async def root():
    return {"message": "Welcome to the AI-Powered Threat Center"}
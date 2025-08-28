from fastapi import FastAPI
from src.usecases.schemas import PredictRequestDTO
from src.usecases.predict_response import PredictResponseUseCase
from src.ml.inference import FraudPredictor
from src.infra.config import settings

app = FastAPI(title="Fraud Detection API")

# Inyección de dependencias
predictor_impl = FraudPredictor(settings.MODEL_DIR)
usecase = PredictResponseUseCase(predictor_impl, threshold=settings.THRESHOLD)

@app.post("/predict")
def predict_endpoint(request: PredictRequestDTO):
    return usecase.execute(request.dict())
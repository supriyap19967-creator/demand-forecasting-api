from fastapi import FastAPI
from pydantic import BaseModel
from predictor import predict_demand

app = FastAPI(title="Demand Forecasting API")

class PredictionRequest(BaseModel):
    lag_1: float

class PredictionResponse(BaseModel):
    predicted_demand: float

@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):
    prediction = predict_demand(request.lag_1)
    return {"predicted_demand": prediction}

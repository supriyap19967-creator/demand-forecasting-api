from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from predictor import predict_demand, model_info
import time
import os

app = FastAPI(title="Demand Forecasting API")

class PredictionRequest(BaseModel):
    lag_1: float

class PredictionResponse(BaseModel):
    predicted_demand: float


@app.post("/predict", response_model=PredictionResponse)
def predict(request: PredictionRequest):

    # 🚫 Failure case 1
    if request.lag_1 < 0:
        raise HTTPException(status_code=400, detail="lag_1 cannot be negative")

    if request.lag_1 > 1_000_000:
        raise HTTPException(status_code=400, detail="lag_1 value is unrealistically large")

    if request.lag_1 == 0:
        raise HTTPException(status_code=400, detail="lag_1 cannot be zero")

    # 📉 Drift awareness (INSIDE function)
    training_mean = model_info.get("training_mean_demand")
    training_std = model_info.get("training_std_demand")

    if training_mean and training_std:
        deviation = abs(request.lag_1 - training_mean)
        if deviation > 3 * training_std:
            print("WARNING: Potential data drift detected")

    # ⏱ Latency tracking
    start = time.time()
    prediction = predict_demand(request.lag_1)
    end = time.time()

    print(f"Inference latency: {end - start:.6f} seconds")

    return {"predicted_demand": prediction}


@app.get("/model-info")
def get_model_info():
    return model_info


if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("app:app", host="0.0.0.0", port=port)

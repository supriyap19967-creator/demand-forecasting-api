
import os
import json

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
model_path = os.path.join(BASE_DIR, "model_info.json")

with open(model_path, "r") as f:
    model_info = json.load(f)


def predict_demand(lag_1: float) -> float:
    return float(lag_1)

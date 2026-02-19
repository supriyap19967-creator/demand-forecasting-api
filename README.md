# demand-forecasting-api

## Overview
This project implements a **production-ready demand forecasting system** using historical time-series data.
The final solution is exposed as a **REST API** and deployed on **Google Cloud Run**.

The focus of this project is on:
- Time-series thinking
- Proper model evaluation
- Production deployment using cloud services

---

## Problem Statement
Forecast **weekly demand** using historical demand patterns.

Such forecasting problems are common in:
- Inventory planning
- Supply chain optimization
- Retail operations
- Capacity planning

The goal is to predict the **next period’s demand** based on past behavior.

---

## Data Engineering
- Raw demand data was aggregated to **weekly demand**
- Ensured **time continuity** (no missing weeks)
- Handled missing and inconsistent values
- Created a clean time-series dataset suitable for forecasting

---
**Core columns:**
center_id | week | total_demand

--

## Feature Engineering
Time-based feature engineering was applied to capture temporal patterns.

### Time Features
- Week of year
- Month (derived from week index)

### Lag Features
- `lag_1`: demand from the previous week
- `lag_4`: demand from four weeks ago

### Rolling Features
- `rolling_mean_4`: 4-week rolling average (shifted to avoid data leakage)

These features help capture:
- Short-term demand memory
- Trends
- Seasonality

---

## Train–Validation Strategy
- **Time-based split** (no random shuffling)
- Most recent weeks used for validation
- Prevents data leakage
- Mimics real-world forecasting conditions

---

## Model Evaluation
Multiple models were evaluated:

| Model | Result |
|------|--------|
| Naive Baseline (lag-1) | ✅ Best |
| Random Forest | Higher error |
| Boosting models | No improvement |

### Final Model Choice
The **baseline lag-based model** performed best due to strong temporal persistence in demand.

**Why baseline was chosen:**
- Lower validation error
- Simple and stable
- Easy to explain and maintain in production

This reflects real industry practice where simpler models are preferred when they perform well.

---

## API Design
The forecasting logic is exposed via a REST API.

### Endpoint

POST /predict

## Production Enhancements

- Input validation and explicit failure handling (negative, zero, unrealistic values)
- Lightweight data drift awareness using training distribution statistics
- Inference latency logging
- Model metadata endpoint (/model-info)
- Cloud-native deployment on Google Cloud Run
- Containerized with Docker

## Failure Handling

The API explicitly handles:
- Negative inputs
- Zero values
- Unrealistic large values
- Drift detection warnings

## Rollback Strategy

If a new model version underperforms in production:

1. Revert to previous `model_info.json` version.
2. Redeploy the last stable container image from Artifact Registry.
3. Validate using the `/model-info` endpoint.
4. Confirm health via `/health` and sample `/predict` requests.

This ensures safe rollback without service interruption.

### Request
```json
{
  "lag_1": 25000
}
Response
{
  "predicted_demand": 25000.0
}



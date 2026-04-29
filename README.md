# 🤖 Rythma AI Microservice

Machine-learning powered activity recommendations & menstrual-cycle–aware insights.

This microservice powers personalised movement guidance inside the **Rythma** app.

It loads trained ML models (stored with **Git LFS**) and exposes a FastAPI endpoint returning daily recommendations.

## Project Structure

```
AI/
├── Dockerfile
├── data/
│   ├── health_fitness.csv
│   └── latest.csv
├── models/
│   ├── fitted_pipeline.pkl
│   └── rf_activity_87pct.pkl
├── notebooks/
│   ├── 01_data_import_and_quality.ipynb
│   ├── 02_feature_exploration_and_analysis.ipynb
│   ├── 03_baseline_model.ipynb
│   ├── 04_menstrual_model.ipynb
│   └── Untitled.ipynb
└── production/
    ├── app.py
    ├── config.py
    ├── generate_recommendation.py
    ├── menstrual_phase.py
    ├── preprocess_and_predict.py
    ├── sentence_mapping.py
    ├── requirements.txt
```

# Setup Instructions

## 1️⃣ Install Git LFS (Required!)

The ML models are too large for normal Git and are stored using **Git LFS**.

### macOS

```sh
brew install git-lfs
git lfs install
```

### Windows

```sh
choco install git-lfs
git lfs install
```

### Linux

```sh
sudo apt install git-lfs
git lfs install
```

### Verify model files downloaded correctly

```sh
git lfs ls-files
```

Expected:

```
AI/models/fitted_pipeline.pkl
AI/models/rf_activity_87pct.pkl
```

If missing:

```sh
git lfs pull
```

<br>

# Running the AI Microservice (Docker)

## 2️⃣ Build the container

```sh
docker build -t ai-service .
```

## 3️⃣ Start the microservice

```sh
docker run -d -p 8005:8005 ai-service
```

Check:

```sh
docker ps
```

<br>

# Testing the API

## Health Check

```sh
curl http://localhost:8005/
```

## Prediction Request

```sh
curl -X POST http://localhost:8005/predict   -H "Content-Type: application/json"   -d '{
  "age": 27,
  "gender": "F",
  "height_cm": 168,
  "weight_kg": 62,
  "duration_minutes": 55,
  "intensity": "Medium",
  "calories_burned": 8.5,
  "hours_sleep": 7.5,
  "stress_level": 3,
  "daily_steps": 10000,
  "hydration_level": 2.6,
  "days_since_last_period": 3
}'
```

<br>

# How It Works

- **fitted_pipeline.pkl** — preprocessing transforms
- **rf_activity_87pct.pkl** — Random Forest activity model
- **menstrual_phase.py** — computes menstrual phase + score
- **sentence_mapping.py** — converts predictions to sentences
- **app.py** — FastAPI microservice (`POST /predict`)

<br>

# Docker Maintenance

Stop containers:

```sh
docker stop $(docker ps -q)
```

Remove containers:

```sh
docker rm $(docker ps -aq)
```

<br>

# Notebooks

- EDA
- Baseline modelling
- Pipeline creation
- Menstrual-cycle model
- Final export

<br>

# App Integration

Frontend calls:

```
http://localhost:8005/predict
```

<br>

# Troubleshooting

### Missing model files

```sh
git lfs install
git lfs pull
```

### Container exits (Error 137)

- Restart Docker Desktop
- Close VS Code/browser
- Rebuild image

### Port 8005 in use

```sh
docker stop <container_id>
```

# Import FastAPI packages
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Import internal ML + recommendation modules
from production import preprocess_and_predict
from production import generate_recommendation

# Create the FastAPI application instance
app = FastAPI()

# Allow the app frontend to call this microservice (CORS).
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",

    "http://localhost:5173",
    "http://127.0.0.1:5173",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,      
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



@app.post("/recommend")
def recommend(user: dict):
    """
    Generate an activity prediction and a personalized movement
    recommendation based on user input data.

    Args:
        user (dict): User features such as sleep, gender, mood, 
        and menstrual cycle details.

    Returns:
        dict: {
            "activity": str - predicted activity category e.g. HIIT,
            "recommendation": str - tailored movement suggestion
        }
    """
    activity = preprocess_and_predict.predict(user)
    sentence = generate_recommendation.generate_sentence(user, activity)
    return {
        "activity": activity,
        "recommendation": sentence
    }

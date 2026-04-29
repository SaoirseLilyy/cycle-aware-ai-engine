import joblib
import pandas as pd
import numpy as np

from production.config import MODELS_DIR
from production.menstrual_phase import MenstrualPhaseConverter

# Load pipeline and model
pipeline = joblib.load(MODELS_DIR / "fitted_pipeline.pkl")

MODEL = joblib.load(MODELS_DIR / "rf_activity_87pct.pkl")


def preprocess_user_input(user_json):
    """
    Preprocess raw user input into a numerical feature vector
    suitable for the ML activity prediction model.

    Processing steps:
    1. Convert user JSON into a DataFrame
    2. Extract menstrual cycle information (days + gender)
    3. Convert cycle day → menstrual phase score (0–3, or -1 fallback)
    4. Apply the scikit-learn preprocessing pipeline
    5. Remove gender one-hot-encoded columns
    6. Append the menstrual phase score as the final feature

    Args:
        user_json (dict): Raw input data from the frontend.

    Returns:
        np.ndarray: The processed feature array.
    """
    
    # Convert user JSON to dataframe
    df = pd.DataFrame([user_json])

    # Extract menstrual details
    day = user_json.get("days_since_last_period")
    gender = user_json.get("gender")

    # Compute menstrual phase score (get_intensity())
    conv = MenstrualPhaseConverter(day=day, gender=gender)
    phase_encoded = conv.get_intensity()

    # Transform normal user features
    X = pipeline.named_steps["preprocessor"].transform(df)


    # Remove gender columns
    feature_names = pipeline.named_steps["preprocessor"].get_feature_names_out()
    gender_cols = [
        "onehot__gender_F",
        "onehot__gender_M",
        "onehot__gender_Other",
    ]
    gender_idx = [i for i, name in enumerate(feature_names) if name in gender_cols]

    X = np.delete(X, gender_idx, axis=1)

    # Append menstrual intensity feature
    X = np.hstack([X, [[phase_encoded]]])

    return X



def predict(user_json):
    """
    Run the ML model to predict an activity category.

    Args:
        user_json (dict): Raw user data.

    Returns:
        str: Predicted activity class label.
    """
    X = preprocess_user_input(user_json)
    return MODEL.predict(X)[0]

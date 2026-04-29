from pathlib import Path

# Root directory of the AI service
ROOT = Path(__file__).resolve().parents[1]

# Directory containing training data
DATA_DIR = ROOT / "data"

# Directory containing trained model and preprocessing (.pkl files)
MODELS_DIR = ROOT / "models"

from pathlib import Path

# ------------------- PATH CONSTANTS -------------------
constants_path = Path(__file__)
SRC_PATH = constants_path.parent
PROJECT_PATH = SRC_PATH.parent
DATA_PATH = PROJECT_PATH / "data"
RAW_PATH = DATA_PATH / "raw"
PROCESSED_PATH = DATA_PATH / "processed"

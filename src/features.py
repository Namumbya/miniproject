"""Single source of truth for model inputs, shared by training and the app."""
import pandas as pd

BINARY_FEATURES = {
    "SMOKING": "Do you smoke?",
    "YELLOW_FINGERS": "Do you have yellow fingers or nails?",
    "ANXIETY": "Do you have anxiety?",
    "CHRONIC DISEASE": "Do you have a chronic disease?",
    "FATIGUE": "Do you have persistent fatigue?",
    "ALLERGY": "Do you have a persistent allergy?",
    "WHEEZING": "Do you experience wheezing?",
    "ALCOHOL CONSUMING": "Do you consume alcohol?",
    "COUGHING": "Do you have a persistent cough?",
    "SHORTNESS OF BREATH": "Do you experience shortness of breath?",
    "SWALLOWING DIFFICULTY": "Do you have difficulty swallowing?",
    "CHEST PAIN": "Do you experience chest pain?",
}
FEATURES = ["GENDER", "AGE", *BINARY_FEATURES]
TARGET = "LUNG_CANCER"


def load_survey(path: str) -> pd.DataFrame:
    """Load the survey CSV, clean it and encode it as 0/1 (1 = yes / male)."""
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip()
    df = df.drop_duplicates().drop(columns=["PEER_PRESSURE"])
    df["GENDER"] = (df["GENDER"] == "M").astype(int)
    for col in BINARY_FEATURES:
        df[col] = (df[col] == 2).astype(int)  # survey codes: 2 = yes, 1 = no
    df[TARGET] = (df[TARGET] == "YES").astype(int)
    return df[FEATURES + [TARGET]]


def encode_answers(age: int, male: bool, answers: dict[str, bool]) -> pd.DataFrame:
    """Build the one-row model input from app answers, in training column order."""
    row = {"GENDER": int(male), "AGE": age, **{k: int(answers[k]) for k in BINARY_FEATURES}}
    return pd.DataFrame([row], columns=FEATURES)

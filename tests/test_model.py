import json
from pathlib import Path

import joblib

from src.features import BINARY_FEATURES, FEATURES, encode_answers, load_survey

ROOT = Path(__file__).resolve().parent.parent


def test_training_data_is_clean():
    df = load_survey(str(ROOT / "survey lung cancer.csv"))
    assert not df.duplicated().any()
    assert list(df.columns[:-1]) == FEATURES
    assert df[FEATURES].isin([0, 1]).all().drop("AGE").all()


def test_app_input_matches_model_features():
    X = encode_answers(60, True, {k: False for k in BINARY_FEATURES})
    assert list(X.columns) == FEATURES
    model = joblib.load(ROOT / "models" / "model.joblib")
    assert model.n_features_in_ == len(FEATURES)
    assert 0.0 <= model.predict_proba(X)[0, 1] <= 1.0


def test_symptoms_raise_risk():
    model = joblib.load(ROOT / "models" / "model.joblib")
    none = encode_answers(60, True, {k: False for k in BINARY_FEATURES})
    many = encode_answers(60, True, {k: True for k in BINARY_FEATURES})
    assert model.predict_proba(many)[0, 1] > model.predict_proba(none)[0, 1]


def test_metrics_record_training_versions():
    m = json.loads((ROOT / "models" / "metrics.json").read_text())
    assert m["features"] == FEATURES

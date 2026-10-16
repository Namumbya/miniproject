import json
from pathlib import Path

import joblib
import numpy as np
import pytest

from src.explain import contributions
from src.features import BINARY_FEATURES, FEATURES, encode_answers, load_survey
from src.train import choose_cutoffs, tier_table

ROOT = Path(__file__).resolve().parent.parent


@pytest.fixture(scope="module")
def model():
    return joblib.load(ROOT / "models" / "model.joblib")


def test_training_data_is_clean():
    df = load_survey(str(ROOT / "survey lung cancer.csv"))
    assert not df.duplicated().any()
    assert list(df.columns[:-1]) == FEATURES
    assert df[FEATURES].isin([0, 1]).all().drop("AGE").all()


def test_app_input_matches_model_features(model):
    X = encode_answers(60, True, {k: False for k in BINARY_FEATURES})
    assert list(X.columns) == FEATURES
    assert model.n_features_in_ == len(FEATURES)
    assert 0.0 <= model.predict_proba(X)[0, 1] <= 1.0


def test_symptoms_raise_risk(model):
    none = encode_answers(60, True, {k: False for k in BINARY_FEATURES})
    many = encode_answers(60, True, {k: True for k in BINARY_FEATURES})
    assert model.predict_proba(many)[0, 1] > model.predict_proba(none)[0, 1]


def test_explanations_add_up_to_the_model_output(model):
    X = encode_answers(70, False, {k: i % 2 == 0 for i, k in enumerate(BINARY_FEATURES)})
    total = contributions(model, X).sum() + model.named_steps["logisticregression"].intercept_[0]
    assert total == pytest.approx(model.decision_function(X)[0])


def test_metrics_match_the_model_and_tiers_are_ordered():
    m = json.loads((ROOT / "models" / "metrics.json").read_text())
    assert m["features"] == FEATURES
    assert m["cutoffs"]["low"] <= m["cutoffs"]["high"]
    # The point of the tiers: few healthy people in "higher", few sick people in "lower".
    assert m["tiers"]["without_cancer"]["higher"] <= 0.15
    assert m["tiers"]["with_cancer"]["lower"] <= 0.10


def test_cutoff_logic_on_toy_scores():
    y = np.array([0] * 10 + [1] * 20)
    p = np.concatenate([np.linspace(0.0, 0.5, 10), np.linspace(0.4, 1.0, 20)])
    low, high = choose_cutoffs(y, p)
    assert low <= high
    t = tier_table(y, p, low, high)
    assert t["with_cancer"]["lower"] <= 0.05 + 1e-9
    assert t["without_cancer"]["higher"] <= 0.10 + 1e-9

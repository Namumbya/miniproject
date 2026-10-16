"""Train, evaluate (cross-validated) and save the risk-screening model.

Usage: python -m src.train
"""
import json
from pathlib import Path

import joblib
import sklearn
from sklearn.calibration import CalibratedClassifierCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import average_precision_score, brier_score_loss, recall_score, roc_auc_score
from sklearn.model_selection import StratifiedKFold, cross_val_predict

from src.features import FEATURES, TARGET, load_survey

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "survey lung cancer.csv"
OUT = ROOT / "models"


def make_model() -> CalibratedClassifierCV:
    rf = RandomForestClassifier(n_estimators=300, min_samples_leaf=2, class_weight="balanced", random_state=42)
    return CalibratedClassifierCV(rf, method="sigmoid", cv=5)


def main() -> None:
    df = load_survey(str(DATA))
    X, y = df[FEATURES], df[TARGET]
    cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

    # Out-of-fold predictions: every row is scored by a model that never saw it.
    proba = cross_val_predict(make_model(), X, y, cv=cv, method="predict_proba")[:, 1]
    threshold = 0.5
    pred = proba >= threshold
    metrics = {
        "rows": int(len(df)),
        "positives": int(y.sum()),
        "recall": round(float(recall_score(y, pred)), 3),
        "specificity": round(float(recall_score(y, pred, pos_label=0)), 3),
        "roc_auc": round(float(roc_auc_score(y, proba)), 3),
        "pr_auc": round(float(average_precision_score(y, proba)), 3),
        "brier": round(float(brier_score_loss(y, proba)), 3),
        "threshold": threshold,
        "sklearn_version": sklearn.__version__,
        "features": FEATURES,
    }

    model = make_model().fit(X, y)
    OUT.mkdir(exist_ok=True)
    joblib.dump(model, OUT / "model.joblib")
    (OUT / "metrics.json").write_text(json.dumps(metrics, indent=2))
    print(json.dumps(metrics, indent=2))


if __name__ == "__main__":
    main()

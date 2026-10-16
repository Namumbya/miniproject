"""Exact per-prediction explanations for the logistic-regression pipeline.

For a linear model with independent features the SHAP value of feature i is
coef_i * (x_i - mean_i) / scale_i, so no extra dependency is needed.
Contributions are in log-odds relative to the average respondent.
"""
import numpy as np
import pandas as pd
from sklearn.pipeline import Pipeline


def contributions(model: Pipeline, X: pd.DataFrame) -> pd.Series:
    scaler, clf = model.named_steps["standardscaler"], model.named_steps["logisticregression"]
    z = scaler.transform(X)[0]
    return pd.Series(clf.coef_[0] * z, index=X.columns).sort_values(key=np.abs, ascending=False)

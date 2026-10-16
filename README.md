# Lung Cancer Risk Screening

Educational Streamlit app that estimates lung-cancer risk from 14 survey answers. **Not a diagnosis.**

## Run
```
uv sync
uv run python -m src.train      # trains, cross-validates, writes models/model.joblib + metrics.json
uv run streamlit run app.py
uv run pytest
```

## Layout
- `src/features.py` – feature list and encoding shared by training and the app (prevents train/serve mismatch)
- `src/train.py` – deduplicates, trains a calibrated RandomForest, reports 5-fold out-of-fold metrics
- `app.py` – the Streamlit UI
- `models/` – saved model and `metrics.json`
- `notebooks/` – original exploration notebooks

## Model limits
276 unique survey rows (only 38 without cancer). Cross-validated recall is high (~0.96) but specificity is low
(~0.47): the model flags many healthy people. See `models/metrics.json`. Do not use for clinical decisions.

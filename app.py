import json
from pathlib import Path

import joblib
import streamlit as st

from src.features import BINARY_FEATURES, encode_answers

MODELS = Path(__file__).parent / "models"

st.set_page_config(page_title="Lung Cancer Risk Screening", page_icon="🫁")


@st.cache_resource
def load_model():
    return joblib.load(MODELS / "model.joblib")


st.title("Lung Cancer Risk Screening")
st.warning(
    "This is an educational screening aid, **not a diagnosis**. It was trained on a small "
    "survey dataset (276 people). Only a clinician can assess your health."
)

with st.form("inputs"):
    age = st.number_input("Age", min_value=18, max_value=100, value=50)
    sex = st.radio("Sex", ["Female", "Male"], horizontal=True)
    answers = {key: st.radio(q, ["No", "Yes"], horizontal=True) == "Yes" for key, q in BINARY_FEATURES.items()}
    submitted = st.form_submit_button("Estimate risk")

if submitted:
    X = encode_answers(age, sex == "Male", answers)
    p = float(load_model().predict_proba(X)[0, 1])
    st.metric("Estimated risk score", f"{p:.0%}")
    if p >= 0.5:
        st.error("Higher risk pattern. Please discuss these symptoms with a doctor.")
    else:
        st.success("Lower risk pattern. If you have symptoms or worries, still see a doctor.")
    st.caption("Inputs are processed in this session only and are not stored or emailed.")

with st.expander("About the model"):
    st.json(json.loads((MODELS / "metrics.json").read_text()))

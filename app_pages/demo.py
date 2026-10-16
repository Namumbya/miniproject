import json
from pathlib import Path

import joblib
import streamlit as st

from src.explain import contributions
from src.features import BINARY_FEATURES, encode_answers

MODELS = Path(__file__).resolve().parent.parent / "models"


@st.cache_resource
def load_model():
    return joblib.load(MODELS / "model.joblib")


@st.cache_data
def load_metrics() -> dict:
    return json.loads((MODELS / "metrics.json").read_text())


metrics = load_metrics()
cutoffs = metrics["cutoffs"]

st.title("Symptom model demo")
st.warning(
    "A machine-learning experiment, not a diagnosis. It was trained on a small survey "
    f"dataset ({metrics['rows']} people) and has not been clinically validated. Do not use it to judge your health.",
    icon=":material/warning:",
)

with st.form("inputs"):
    age = st.number_input("Age", min_value=18, max_value=100, value=50)
    sex = st.segmented_control("Sex", ["Female", "Male"], default="Female", required=True)
    answers = {
        key: st.segmented_control(question, ["No", "Yes"], default="No", required=True, key=key) == "Yes"
        for key, question in BINARY_FEATURES.items()
    }
    submitted = st.form_submit_button("Check pattern", icon=":material/search:", type="primary")

if submitted:
    X = encode_answers(age, sex == "Male", answers)
    model = load_model()
    score = float(model.predict_proba(X)[0, 1])

    if score < cutoffs["low"]:
        st.success(
            "Your answers look like most healthy respondents. If you have symptoms or worries, "
            "still see a doctor.",
            title="Lower-risk pattern",
        )
    elif score < cutoffs["high"]:
        st.info(
            "Your answers sit between the two groups, so this tool cannot tell. If any symptom "
            "is new or lasting more than a few weeks, talk to a doctor.",
            title="Uncertain pattern",
        )
    else:
        st.error(
            "Your answers resemble people in the survey who had lung cancer. This does not mean "
            "you have it. Please discuss these symptoms with a doctor.",
            title="Higher-risk pattern",
        )

    st.subheader("What drove this result")
    contrib = contributions(model, X)
    top = contrib.head(6).rename(lambda f: f.replace("_", " ").capitalize())
    st.bar_chart(
        top.rename("Effect on score").to_frame(),
        horizontal=True,
        alt="Bar chart of the six answers that pushed the score up (right) or down (left)",
    )
    st.caption("Bars to the right raise the score, bars to the left lower it, compared with an average respondent.")
    st.caption("Answers are processed in this session only and are not stored or emailed.")

with st.expander("About the model"):
    tiers = metrics["tiers"]
    st.markdown(
        f"- **Model:** logistic regression on {len(metrics['features'])} answers.\n"
        f"- **Accuracy (cross-validated):** ROC-AUC {metrics['roc_auc']} "
        f"(95% CI {metrics['auc_ci95'][0]} to {metrics['auc_ci95'][1]}).\n"
        f"- **Healthy respondents:** {tiers['without_cancer']['lower']:.0%} lower, "
        f"{tiers['without_cancer']['uncertain']:.0%} uncertain, {tiers['without_cancer']['higher']:.0%} higher "
        f"(only {metrics['rows'] - metrics['positives']} healthy people in the data, so this is noisy).\n"
        f"- **Respondents with cancer:** {tiers['with_cancer']['lower']:.0%} lower, "
        f"{tiers['with_cancer']['uncertain']:.0%} uncertain, {tiers['with_cancer']['higher']:.0%} higher.\n"
        "- The score is relative to this survey, where 86% of people had cancer. It is not your "
        "real-world probability of having cancer."
    )
    st.caption("Full details are in models/MODEL_CARD.md.")

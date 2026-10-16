import streamlit as st

st.title("Lung cancer screening, explained")
st.warning(
    "This project is educational. It does not diagnose anything and it is not a medical device.",
    icon=":material/warning:",
)

st.subheader("What matters for lung cancer risk")
st.markdown(
    "Guidelines decide who should be screened mainly by **age** and **smoking history** (how much, and how "
    "long ago). Symptoms such as cough, wheezing or chest pain tend to appear later and are common in many "
    "harmless conditions, so they are a poor basis for screening."
)

st.subheader("What is in this app")
with st.container(border=True):
    st.markdown("**:material/fact_check: Guideline example (US)**")
    st.write(
        "Implements one published guideline (USPSTF 2021) so you can see how age and pack-years decide "
        "eligibility. Criteria differ by country, so treat it as a worked example, not advice for everywhere."
    )
with st.container(border=True):
    st.markdown("**:material/experiment: Symptom model demo**")
    st.write(
        "A machine-learning experiment on a small public survey (276 people, 86% with cancer, unknown origin). "
        "It shows how such a model is built, evaluated and explained, including its limits. "
        "Do not use it to judge your own health."
    )

st.subheader("If you are worried")
st.markdown(
    "- See a doctor about any symptom that is new or lasts more than a few weeks, whatever this app says.\n"
    "- Screening rules differ by country and change over time; ask your clinician or national screening programme.\n"
    "- Quitting smoking lowers risk at any age."
)

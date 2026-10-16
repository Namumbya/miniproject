import streamlit as st

from src.eligibility import MAX_YEARS_SINCE_QUIT, MIN_AGE, MIN_PACK_YEARS, MAX_AGE, assess

st.title("Guideline example: US screening criteria")
st.info(
    "Screening criteria depend on where you live and change over time. This page implements one published "
    "US guideline so you can see how age and pack-years work. It is not advice for every country.",
    icon=":material/public:",
)
st.caption(
    f"US Preventive Services Task Force 2021 (grade B): adults aged {MIN_AGE} to {MAX_AGE} with at least "
    f"{MIN_PACK_YEARS} pack-years who smoke now or quit within the past {MAX_YEARS_SINCE_QUIT} years. "
    "Screening test: annual low-dose CT."
)

with st.form("eligibility"):
    age = st.number_input("Age", min_value=18, max_value=100, value=55)
    status = st.segmented_control(
        "Smoking status", ["Current", "Former", "Never"], default="Current", required=True, key="status"
    )
    packs = st.number_input("Packs per day (1 pack = 20 cigarettes)", min_value=0.0, max_value=10.0, value=1.0, step=0.25)
    years = st.number_input("Years smoked", min_value=0, max_value=80, value=20)
    quit_years = st.number_input("Years since quitting (former smokers)", min_value=0, max_value=80, value=0)
    submitted = st.form_submit_button("Check eligibility", icon=":material/fact_check:", type="primary")

if submitted:
    result = assess(age, status.lower(), packs, years, quit_years)
    if status != "Never":
        st.metric("Smoking history", f"{result.pack_years:g} pack-years", help="Packs per day times years smoked")
    if result.eligible:
        st.success(
            "Your answers meet the USPSTF criteria. Ask a doctor whether screening applies where you live; "
            "health problems that limit life expectancy can also change the advice.",
            title="Meets the US criteria",
        )
    else:
        st.info(
            "\n".join(f"- {r}" for r in result.reasons)
            + "\n\nOther guidelines and personal risk factors (family history, COPD, asbestos) can differ, "
            "so a clinician's view still matters.",
            title="Does not meet the US criteria",
        )

st.subheader("Elsewhere")
st.markdown(
    "- Pack-years (packs per day times years smoked) is used by most guidelines; the age range, pack-year "
    "threshold and years-since-quitting cut-off are what differ.\n"
    "- Ask your national or regional screening programme or your clinician which criteria apply to you.\n"
    "- Background: [WHO lung cancer fact sheet](https://www.who.int/news-room/fact-sheets/detail/lung-cancer)."
)

import streamlit as st

st.set_page_config(page_title="Lung cancer screening explained", page_icon=":material/pulmonology:")

page = st.navigation(
    [
        st.Page("app_pages/about.py", title="Start here", icon=":material/info:"),
        st.Page("app_pages/eligibility.py", title="Guideline example (US)", icon=":material/fact_check:"),
        st.Page("app_pages/demo.py", title="Symptom model demo", icon=":material/experiment:"),
    ]
)
page.run()

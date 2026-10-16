from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.features import BINARY_FEATURES

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def open_page(page: str) -> AppTest:
    at = AppTest.from_file(APP, default_timeout=30).run()  # entrypoint first so st.navigation registers pages
    if page:
        at.switch_page(page).run()
    assert not at.exception
    return at


def test_start_page_has_disclaimer():
    at = open_page("")
    assert at.title[0].value == "Lung cancer screening, explained"
    assert at.warning


def test_eligibility_page_eligible_and_not():
    at = open_page("app_pages/eligibility.py")
    at.form_submit_button[0].click().run()  # defaults: 55, current, 1 ppd x 20 years = 20 pack-years
    assert not at.exception and at.success

    at = open_page("app_pages/eligibility.py")
    at.session_state["status"] = "Never"
    at.form_submit_button[0].click().run()
    assert not at.exception and at.info and not at.success


def test_demo_default_answers_not_flagged_higher():
    at = open_page("app_pages/demo.py")
    assert at.warning  # "not a diagnosis" banner
    at.form_submit_button[0].click().run()
    assert not at.exception
    assert not at.error


def test_demo_all_symptoms_flagged_higher_with_explanation():
    at = open_page("app_pages/demo.py")
    for key in BINARY_FEATURES:
        at.session_state[key] = "Yes"
    at.form_submit_button[0].click().run()
    assert not at.exception
    assert at.error
    assert at.get("vega_lite_chart")  # contribution chart rendered

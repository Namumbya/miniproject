from pathlib import Path

from streamlit.testing.v1 import AppTest

from src.features import BINARY_FEATURES

APP = str(Path(__file__).resolve().parent.parent / "app.py")


def run_app() -> AppTest:
    return AppTest.from_file(APP, default_timeout=30).run()


def test_app_loads_with_disclaimer_and_no_result_yet():
    at = run_app()
    assert not at.exception
    assert at.warning  # "not a diagnosis" banner
    assert not at.success and not at.error


def test_no_symptoms_is_not_flagged_higher():
    at = run_app()
    at.form_submit_button[0].click().run()
    assert not at.exception
    assert not at.error  # default answers must not trigger the higher-risk alert


def test_all_symptoms_flagged_higher_with_explanation():
    at = run_app()
    for key in BINARY_FEATURES:
        at.session_state[key] = "Yes"
    at.form_submit_button[0].click().run()
    assert not at.exception
    assert at.error
    assert at.get("vega_lite_chart")  # contribution chart rendered

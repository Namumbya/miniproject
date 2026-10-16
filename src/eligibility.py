"""USPSTF 2021 lung cancer screening eligibility (grade B, annual low-dose CT).

Source: https://www.uspreventiveservicestaskforce.org/uspstf/recommendation/lung-cancer-screening
"Adults aged 50 to 80 years who have a 20 pack-year smoking history and currently smoke
or have quit within the past 15 years."
"""
from dataclasses import dataclass

MIN_AGE, MAX_AGE = 50, 80
MIN_PACK_YEARS = 20
MAX_YEARS_SINCE_QUIT = 15


@dataclass(frozen=True)
class Assessment:
    eligible: bool
    pack_years: float
    reasons: tuple[str, ...]  # why not eligible; empty when eligible


def assess(age: int, status: str, packs_per_day: float = 0, years_smoked: float = 0, years_since_quit: float = 0) -> Assessment:
    """status is 'current', 'former' or 'never'."""
    pack_years = round(packs_per_day * years_smoked, 1) if status != "never" else 0.0
    reasons = []
    if not MIN_AGE <= age <= MAX_AGE:
        reasons.append(f"Age is outside {MIN_AGE} to {MAX_AGE}.")
    if status == "never":
        reasons.append("Screening is aimed at people who have smoked.")
    else:
        if pack_years < MIN_PACK_YEARS:
            reasons.append(f"Smoking history is {pack_years:g} pack-years; the guideline starts at {MIN_PACK_YEARS}.")
        if status == "former" and years_since_quit > MAX_YEARS_SINCE_QUIT:
            reasons.append(f"Quit more than {MAX_YEARS_SINCE_QUIT} years ago.")
    return Assessment(not reasons, pack_years, tuple(reasons))

import pytest

from src.certificate_service import Participant, certificate_html


def test_certificate_requires_completed_hours():
    participant = Participant("Lee", "Meal delivery", completed_hours=12, required_hours=20)
    with pytest.raises(ValueError, match="not completed"):
        certificate_html(participant)


def test_certificate_html_records_program_and_hours():
    participant = Participant("Lee", "Meal delivery", completed_hours=20)
    html = certificate_html(participant)
    assert "Lee" in html
    assert "Meal delivery" in html
    assert "20 volunteer hours" in html


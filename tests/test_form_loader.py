import pytest
from visualasic.designer import load_form
from pathlib import Path


def test_load_demo_form():
    p = Path(__file__).resolve().parent.parent / "examples" / "demo.form"
    data = load_form(str(p))
    assert isinstance(data, dict)
    assert data.get("schema_version") == 1
    assert "form" in data
    assert "controls" in data

"""End-to-end checks that the Soul Foods Dash visualiser layout renders."""

import sys
from pathlib import Path

_ROOT = Path(__file__).resolve().parents[1]
if str(_ROOT) not in sys.path:
    sys.path.insert(0, str(_ROOT))

from app import app  # noqa: E402


def test_header_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("h1.app-title", timeout=10)
    title = dash_duo.find_element("h1.app-title")
    assert "Soul Foods" in title.text, "header should show the Soul Foods title"


def test_visualisation_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#sales-chart", timeout=10)
    dash_duo.wait_for_element("#sales-chart .js-plotly-plot", timeout=10)
    assert dash_duo.find_element("#sales-chart") is not None


def test_region_picker_present(dash_duo):
    dash_duo.start_server(app)
    dash_duo.wait_for_element("#region-filter", timeout=10)
    radios = dash_duo.find_elements("#region-filter input[type='radio']")
    assert len(radios) >= 5, "region picker should expose all five options"

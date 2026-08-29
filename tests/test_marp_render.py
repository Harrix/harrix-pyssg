"""Tests for Marp presentation HTML rendering."""

from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch

from harrix_pyssg.marp_render import is_marp_yaml, render_marp_html


def test_is_marp_yaml() -> None:
    """Detect `type: marp` and `marp: true`."""
    assert is_marp_yaml({"type": "marp"})
    assert is_marp_yaml({"marp": True})
    assert is_marp_yaml({"marp": "true"})
    assert not is_marp_yaml({"type": "canvas"})
    assert not is_marp_yaml({})


_MARP_MD = """---
type: marp
marp: true
---

# One

---

# Two
"""


def test_render_marp_html_fallback_splits_slides() -> None:
    """Fallback renderer splits on `---` and emits a slideshow document."""
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "deck.md"
        path.write_text(_MARP_MD, encoding="utf-8")
        with patch("harrix_pyssg.marp_render._render_with_marp_cli", return_value=None):
            html = render_marp_html(path, _MARP_MD)
    assert 'class="slide' in html
    assert "One" in html
    assert "Two" in html
    assert "<!DOCTYPE html>" in html


def test_render_marp_html_includes_slide_text() -> None:
    """CLI or fallback HTML still contains slide headings."""
    with TemporaryDirectory() as tmp:
        path = Path(tmp) / "deck.md"
        path.write_text(_MARP_MD, encoding="utf-8")
        html = render_marp_html(path, _MARP_MD)
    assert "One" in html
    assert "Two" in html
    assert "<!DOCTYPE html>" in html

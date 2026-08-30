"""Tests for the vector-icons catalog section."""

from pathlib import Path
from tempfile import TemporaryDirectory

import harrix_pyssg as hsg

ICONS_ROOT = Path(__file__).parent / "data_icons"
SITE_DATA = Path(__file__).parent / "data_site"


def test_load_icon_families_from_note_folders() -> None:
    """Scan note folders when catalog.json is absent."""
    families = hsg.load_icon_families(ICONS_ROOT)
    ids = {family.icon_id for family in families}
    assert ids == {"building__house", "it__file"}
    house = next(family for family in families if family.icon_id == "building__house")
    assert house.category == "building"
    assert house.lang == "en"
    assert house.rel_output == Path("en") / "icons" / "building" / "building__house"


def test_generate_site_writes_icon_grid_and_family_pages() -> None:
    """Site generation adds /en/icons/ grid plus family pages and a homepage link."""
    md_folder = Path(__file__).parent / "data"
    with TemporaryDirectory() as tmp:
        html_folder = Path(tmp) / "site"
        sg = hsg.StaticSiteGenerator(md_folder, icons_dir=ICONS_ROOT, icons_per_page=1)
        sg.generate_site(html_folder)

        grid = html_folder / "en" / "icons" / "index.html"
        assert grid.is_file()
        text = grid.read_text(encoding="utf8")
        assert "h-icon-grid" in text
        assert "h-icon-card" in text
        assert "File" in text
        page2 = (html_folder / "en" / "icons" / "page" / "2" / "index.html").read_text(encoding="utf8")
        assert "House" in page2
        assert "/en/icons/building/building__house/" in page2
        assert (html_folder / "en" / "icons" / "building" / "index.html").is_file()
        assert (html_folder / "en" / "icons" / "it" / "index.html").is_file()

        family = html_folder / "en" / "icons" / "building" / "building__house"
        assert (family / "index.html").is_file()
        assert (family / "featured-image.svg").is_file()
        assert "House" in (family / "index.html").read_text(encoding="utf8")

        home = (html_folder / "index.html").read_text(encoding="utf8")
        assert "/en/icons/" in home


def test_icon_section_on_content_repo_homepage() -> None:
    """Content-repo homes include an Icons section button."""
    with TemporaryDirectory() as tmp:
        html_folder = Path(tmp) / "site"
        sg = hsg.StaticSiteGenerator(SITE_DATA, icons_dir=ICONS_ROOT)
        sg.generate_site(html_folder)
        home = (html_folder / "ru" / "index.html").read_text(encoding="utf8")
        assert "/en/icons/" in home
        assert (html_folder / "en" / "icons" / "index.html").is_file()

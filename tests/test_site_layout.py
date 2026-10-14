"""Tests for YAML list normalization and taxonomy slug helpers."""

from pathlib import Path

import yaml

import harrix_pyssg as hsg
from harrix_pyssg.site_layout import _MAX_TERM_SLUG_LEN, as_string_list, slugify_term


def test_as_string_list_restores_yaml_key_value_items() -> None:
    """Unquoted `- key: value` YAML items become `key: value` strings."""
    loaded = yaml.safe_load("tags:\n  - Needs: pen and paper\n  - Mobility: high\n  - CSS\n")
    assert as_string_list(loaded["tags"]) == [
        "Needs: pen and paper",
        "Mobility: high",
        "CSS",
    ]


def test_as_string_list_handles_mapping_and_scalars() -> None:
    """Mappings and bare scalars normalize to string lists."""
    assert as_string_list(None) == []
    assert as_string_list("CSS") == ["CSS"]
    assert as_string_list({"Reuse": "once"}) == ["Reuse: once"]
    assert as_string_list([{"Mobility": None}, "  "]) == ["Mobility"]


def test_slugify_term_hashes_overlong_values() -> None:
    """Very long tags get a short stable hash slug under the path limit."""
    long_term = "Needs: " + ("very-long-description-" * 20)
    slug = slugify_term(long_term)
    assert slug.startswith("t-")
    assert len(slug) <= _MAX_TERM_SLUG_LEN
    assert slugify_term(long_term) == slug
    assert slugify_term("CSS") == "CSS"


def test_generate_site_with_yaml_mapping_tags(tmp_path: Path) -> None:
    """Game-style tags with colons create listing folders without WinError 123."""
    md_root = tmp_path / "harrix.dev-games" / "sample-game"
    md_root.mkdir(parents=True)
    (md_root / "sample-game.md").write_text(
        "---\n"
        "date: 2013-07-22\n"
        "categories:\n"
        "  - Psychological game\n"
        "tags:\n"
        "  - Needs: paper (large sheets) and two pens\n"
        "  - Mobility: high\n"
        "lang: ru\n"
        "---\n\n"
        "# Sample game\n\n"
        "Body.\n",
        encoding="utf8",
    )

    html_folder = tmp_path / "site"
    sg = hsg.StaticSiteGenerator(tmp_path, site_title="Harrix")
    sg.generate_site(html_folder)

    tags_root = html_folder / "ru" / "tags"
    assert (tags_root / "index.html").is_file()
    term_dirs = [path for path in tags_root.iterdir() if path.is_dir()]
    assert term_dirs
    assert any((path / "index.html").is_file() for path in term_dirs)
    assert not any("{" in path.name or "'" in path.name for path in term_dirs)

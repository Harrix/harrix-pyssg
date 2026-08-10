"""Tests for ThemeSlicer and PageAssembler."""

from pathlib import Path
from tempfile import TemporaryDirectory

import harrix_pyssg as hsg

THEME_DIST = Path(__file__).parent / "data" / "theme_dist"


def test_theme_slicer_and_page_assembler() -> None:
    """Slice fixture template and assemble pages with/without optional assets."""
    with TemporaryDirectory() as tmp:
        theme_dir = Path(tmp) / "theme"
        slicer = hsg.ThemeSlicer(THEME_DIST, theme_dir, source_html="article.html")
        result = slicer.slice()
        assert result == theme_dir.resolve()
        assert (theme_dir / "manifest.json").is_file()
        assert (theme_dir / "parts" / "head.html").is_file()
        assert (theme_dir / "parts" / "main.html").is_file()
        assert (theme_dir / "parts" / "optional" / "katex_css.html").is_file()
        assert (theme_dir / "css" / "app.css").is_file()
        assert (theme_dir / "js" / "app.js").is_file()

        head = (theme_dir / "parts" / "head.html").read_text(encoding="utf8")
        assert "{{H_SSG_TITLE}}" in head
        assert "{{H_SSG_OPTIONAL_HEAD}}" in head
        assert "katex/katex.css" not in head
        assert "css/app.css" in head

        main = (theme_dir / "parts" / "main.html").read_text(encoding="utf8")
        assert "{{H_SSG_CONTENT}}" in main
        assert "Demo content" not in main

        katex_css = (theme_dir / "parts" / "optional" / "katex_css.html").read_text(encoding="utf8")
        assert "katex/katex.css" in katex_css

        assembler = hsg.PageAssembler(theme_dir)
        plain = assembler.assemble(
            content_html="<h1>Plain</h1><p>Hi</p>",
            title="Plain",
            features=hsg.PageFeatures(),
        )
        assert "<!doctype html>" in plain.lower() or "<!DOCTYPE html>" in plain
        assert "<h1>Plain</h1>" in plain
        assert "Header" in plain
        assert "Footer" in plain
        assert "katex/katex.css" not in plain
        assert "stl-viewer" not in plain
        assert "css/app.css" in plain
        assert "js/app.js" in plain

        with_math = assembler.assemble(
            content_html="<h1>Math</h1><p>$x^2$</p>",
            title="Math",
            features=hsg.PageFeatures(katex=True),
            asset_prefix="../",
        )
        assert "katex/katex.css" in with_math
        assert "katex/katex.js" in with_math
        assert 'href="../css/app.css"' in with_math or 'href=".././css/app.css"' in with_math

        with_stl = assembler.assemble(
            content_html='<div class="h-stl-viewer" data-src="model.stl"></div>',
            title="STL",
            features=hsg.PageFeatures(stl=True),
        )
        assert "stl-viewer/stl-viewer.css" in with_stl
        assert "stl-viewer/stl-viewer.js" in with_stl


def test_detect_page_features() -> None:
    """Detect katex/mermaid/stl features from YAML and content."""
    features = hsg.detect_page_features("<p>Hi</p>", md_content="Hello", yaml_dict={})
    assert features.katex is False
    assert features.stl is False
    assert features.mermaid is False

    features = hsg.detect_page_features("<p>x</p>", md_content="Value $x^2$", yaml_dict={"latex": True})
    assert features.katex is True

    features = hsg.detect_page_features(
        '<pre class="mermaid">graph TD; A-->B;</pre>',
        md_content="```mermaid\ngraph TD; A-->B;\n```",
    )
    assert features.mermaid is True

    features = hsg.detect_page_features(
        '<div class="h-stl-viewer" data-src="a.stl"></div>',
        md_content="",
    )
    assert features.stl is True


def test_generate_html_with_theme() -> None:
    """Article.generate_html wraps content when a theme is provided."""
    md_filename = Path(__file__).parent / "data" / "test_01" / "test_01.md"
    with TemporaryDirectory() as tmp:
        theme_dir = Path(tmp) / "theme"
        html_folder = Path(tmp) / "out"
        hsg.ThemeSlicer(THEME_DIST, theme_dir).slice()

        article = hsg.Article(md_filename)
        article.generate_html(html_folder, theme_dir=theme_dir)

        html = (html_folder / "index.html").read_text(encoding="utf8")
        assert "<nav id=" in html or "Header" in html
        assert "Hello, world!" in html
        assert (html_folder / "css" / "app.css").is_file()
        assert (html_folder / "featured-image.png").is_file()


def test_static_site_generator_with_theme() -> None:
    """StaticSiteGenerator copies theme assets once and prefixes nested pages."""
    md_folder = Path(__file__).parent / "data"
    with TemporaryDirectory() as tmp:
        theme_dir = Path(tmp) / "theme"
        html_folder = Path(tmp) / "site"
        hsg.ThemeSlicer(THEME_DIST, theme_dir).slice()

        sg = hsg.StaticSiteGenerator(md_folder, theme_dir=theme_dir)
        sg.generate_site(html_folder)

        assert (html_folder / "css" / "app.css").is_file()
        nested = html_folder / "test_01" / "index.html"
        assert nested.is_file()
        html = nested.read_text(encoding="utf8")
        assert 'href="../css/app.css"' in html
        assert "Hello, world!" in html

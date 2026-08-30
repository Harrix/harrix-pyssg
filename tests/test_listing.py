"""Tests for site listings, pagination, and content-repo URL layout."""

from pathlib import Path
from tempfile import TemporaryDirectory

import harrix_pyssg as hsg

SITE_DATA = Path(__file__).parent / "data_site"


def test_flat_generate_writes_homepage() -> None:
    """Flat folders still emit articles and a root homepage listing."""
    md_folder = Path(__file__).parent / "data"
    with TemporaryDirectory() as tmp:
        html_folder = Path(tmp) / "site"
        sg = hsg.StaticSiteGenerator(md_folder, per_page=2)
        sg.generate_site(html_folder)

        assert (html_folder / "test_01" / "index.html").is_file()
        home = (html_folder / "index.html").read_text(encoding="utf8")
        assert "Title" in home
        assert 'class="pagination' in home
        assert (html_folder / "page" / "2" / "index.html").is_file()


def test_content_repo_layout_and_listings() -> None:
    """Content-repo folders map to /{lang}/{section}/{year}/{slug}/ plus listings."""
    with TemporaryDirectory() as tmp:
        html_folder = Path(tmp) / "site"
        sg = hsg.StaticSiteGenerator(SITE_DATA, per_page=1, site_title="Harrix")
        sg.generate_site(html_folder)

        assert (html_folder / "ru" / "articles" / "2013" / "alpha" / "index.html").is_file()
        assert (html_folder / "ru" / "articles" / "2013" / "beta" / "index.html").is_file()
        assert not (html_folder / "ru" / "articles" / "2013" / "draft").exists()
        assert (html_folder / "en" / "articles" / "2013" / "alpha" / "index.html").is_file()
        assert (html_folder / "ru" / "games" / "game-one" / "index.html").is_file()

        home = (html_folder / "index.html").read_text(encoding="utf8")
        assert "Harrix" in home
        assert "Beta title" in home
        assert "Draft title" not in home
        assert "/ru/articles/" in home
        assert "/ru/games/" in home

        ru_home = (html_folder / "ru" / "index.html").read_text(encoding="utf8")
        assert "Beta title" in ru_home
        assert (html_folder / "ru" / "page" / "2" / "index.html").is_file()

        articles = (html_folder / "ru" / "articles" / "index.html").read_text(encoding="utf8")
        assert "Статьи" in articles
        assert "/ru/articles/2013/" in articles

        year = (html_folder / "ru" / "articles" / "2013" / "index.html").read_text(encoding="utf8")
        assert "2013" in year
        assert "Alpha title" in year or "Beta title" in year

        games = (html_folder / "ru" / "games" / "index.html").read_text(encoding="utf8")
        assert "Game one" in games

        category = (html_folder / "ru" / "categories" / "it" / "index.html").read_text(encoding="utf8")
        assert "Alpha title" in category or "Beta title" in category

        tag = (html_folder / "ru" / "tags" / "CSS" / "index.html").read_text(encoding="utf8")
        assert "Alpha title" in tag

        en_home = (html_folder / "en" / "index.html").read_text(encoding="utf8")
        assert "Alpha EN" in en_home
        assert "Beta title" not in en_home


def test_place_article_content_repo() -> None:
    """`place_article` parses harrix.dev content repository names."""
    article = hsg.Article(SITE_DATA / "harrix.dev-articles-2013" / "alpha" / "alpha.md")
    placement = hsg.place_article(article, SITE_DATA, hsg.SiteSettings())
    assert placement.lang == "ru"
    assert placement.section == "articles"
    assert placement.year == "2013"
    assert placement.slug == "alpha"
    assert placement.rel_output == Path("ru") / "articles" / "2013" / "alpha"

    game = hsg.Article(SITE_DATA / "harrix.dev-games" / "game-one" / "game-one.md")
    game_placement = hsg.place_article(game, SITE_DATA, hsg.SiteSettings())
    assert game_placement.section == "games"
    assert game_placement.year is None
    assert game_placement.rel_output == Path("ru") / "games" / "game-one"


def test_build_catalog_skips_drafts() -> None:
    """Drafts with `published: false` stay out of listings."""
    sg = hsg.StaticSiteGenerator(SITE_DATA)
    catalog = hsg.build_catalog(sg.articles, SITE_DATA, sg.settings)
    titles = {entry.title for entry in catalog}
    assert "Draft title" not in titles
    assert "Alpha title" in titles
    assert "Game one" in titles

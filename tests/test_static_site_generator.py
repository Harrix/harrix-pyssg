"""Tests for the StaticSiteGenerator class."""

from pathlib import Path
from tempfile import TemporaryDirectory

import harrix_pyssg as hsg


def test_static_site_generator() -> None:
    """Test StaticSiteGenerator for all rules and scenarios."""
    md_folder = "./tests/data"
    html_folder = "./build_site"

    # Test: StaticSiteGenerator initialization
    sg = hsg.StaticSiteGenerator(md_folder)
    assert len(sg.articles) == 3

    # Test: generate_site method creates files
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.generate_site(html_folder)
    count_files = 0
    for item in filter(
        lambda path: not any(part for part in path.parts if part.startswith(".")),
        Path(html_folder).rglob("*"),
    ):
        if item.is_file():
            count_files += 1
    assert count_files == 7

    # Test: generate_site method with html_folder setter
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.html_folder = html_folder
    sg._clear_html_folder_directory()
    sg.generate_site()
    assert (Path(html_folder) / "test_01/index.html").exists()

    # Test: get_set_variables_from_yaml method
    sg = hsg.StaticSiteGenerator(md_folder)
    variables = sg.get_set_variables_from_yaml()
    assert len(variables) == 3
    assert "categories" in variables
    assert "date" in variables
    assert "tags" in variables

    # Test: articles property
    sg = hsg.StaticSiteGenerator(md_folder)
    articles = sg.articles
    assert isinstance(articles, list)
    assert len(articles) == 3
    assert all(isinstance(article, hsg.Article) for article in articles)

    # Test: html_folder property getter and setter
    sg = hsg.StaticSiteGenerator(md_folder)
    assert sg.html_folder is None
    sg.html_folder = html_folder
    assert sg.html_folder is not None
    assert "build_site" in str(sg.html_folder)

    # Test: md_folder property
    sg = hsg.StaticSiteGenerator(md_folder)
    assert sg.md_folder is not None
    assert "data" in str(sg.md_folder)

    # Test: _clear_html_folder_directory method
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_html_folder = temp_path / "test_html"
        test_html_folder.mkdir()
        (test_html_folder / "test_file.txt").write_text("test", encoding="utf8")

        sg = hsg.StaticSiteGenerator(md_folder)
        sg.html_folder = test_html_folder
        sg._clear_html_folder_directory()
        assert test_html_folder.exists()
        assert not (test_html_folder / "test_file.txt").exists()

    # Test: add_image_captions method
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_data_folder = temp_path / "test_data"
        test_data_folder.mkdir()
        test_article_folder = test_data_folder / "test_article"
        test_article_folder.mkdir()
        test_md_file = test_article_folder / "test_article.md"
        test_md_file.write_text(
            """---
date: 2022-09-18
---

# Title

![Alt text](image.png)
""",
            encoding="utf8",
        )

        sg = hsg.StaticSiteGenerator(test_data_folder)
        initial_content = sg.articles[0].md_content
        sg.add_image_captions()
        updated_content = sg.articles[0].md_content
        assert len(updated_content.splitlines()) > len(initial_content.splitlines())

    # Test: add_yaml_tag_to_all_md method
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_data_folder = temp_path / "test_data"
        test_data_folder.mkdir()
        test_article_folder = test_data_folder / "test_article"
        test_article_folder.mkdir()
        test_md_file = test_article_folder / "test_article.md"
        test_md_file.write_text(
            """---
date: 2022-09-18
---

# Title
""",
            encoding="utf8",
        )

        sg = hsg.StaticSiteGenerator(test_data_folder)
        sg.add_yaml_tag_to_all_md(("author", "Test Author"))
        assert sg.articles[0].md_yaml_dict["author"] == "Test Author"

    # Test: generate_site creates correct folder structure
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_html_folder = temp_path / "test_html"

        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(test_html_folder)

        assert (test_html_folder / "test_01/index.html").exists()
        assert (test_html_folder / "test_02/index.html").exists()
        assert (test_html_folder / "test_03/index.html").exists()

    # Test: generate_site copies featured images
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_html_folder = temp_path / "test_html"

        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(test_html_folder)

        assert (test_html_folder / "test_01/featured-image.png").exists()
        assert (test_html_folder / "test_02/featured-image.png").exists()

    # Test: generate_site copies image directories
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        test_html_folder = temp_path / "test_html"

        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(test_html_folder)

        assert (test_html_folder / "test_01/img/test-image.png").exists()
        assert (test_html_folder / "test_02/img/test-image.png").exists()

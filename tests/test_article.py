"""Tests for the Article class."""

import datetime
from pathlib import Path
from tempfile import TemporaryDirectory

import harrix_pyssg as hsg

TEST_MD_CONTENT = """---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---

# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)
"""


TEST_MD_CONTENT_NO_YAML = """# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)
"""


TEST_MD_YAML = """---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---"""


TEST_MD_YAML_DICT = {
    "date": datetime.date(2022, 9, 18),
    "categories": ["it", "web"],
    "tags": ["CSS"],
}


def test_article() -> None:
    """Test Article for all rules and scenarios."""
    md_filename = "./tests/data/test_01/test_01.md"

    # Test: Article initialization and basic properties
    a = hsg.Article(md_filename)
    assert a.md_filename.name == "test_01.md"
    assert len(a.md_content.splitlines()) == len(TEST_MD_CONTENT.splitlines())
    assert len(a.featured_image_filenames) == 1

    # Test: md_content_no_yaml property getter
    md_content_no_yaml_lines = len(a.md_content_no_yaml.splitlines())
    assert md_content_no_yaml_lines > 0

    # Test: md_content_no_yaml property setter
    a.md_content_no_yaml = "# New Title"
    assert len(a.md_content_no_yaml.splitlines()) == 1

    # Test: md_content updates when md_content_no_yaml changes
    len_yaml = len(a.md_yaml.splitlines())
    a.md_content_no_yaml = "# New Title"
    assert len(a.md_content.splitlines()) == len_yaml + 2

    # Test: md_yaml_dict modification updates md_content
    a = hsg.Article(md_filename)
    a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
    assert a.md_content.splitlines()[1] == "date: 2022-11-04"

    # Test: md_yaml_dict modification with lists
    a = hsg.Article(md_filename)
    a.md_yaml_dict["categories"].append("test")
    assert a.md_content.splitlines()[2] == "categories: [it, web, test]"

    # Test: add_image_captions method
    a = hsg.Article(md_filename)
    a.add_image_captions()
    assert len(a.md_content.splitlines()) == 15

    # Test: _get_nocode_code_parts method
    md_filename_code = "./tests/data/test_03/test_03.md"
    a = hsg.Article(md_filename_code)
    from_parts = "\n".join([part[0] for part in a._get_nocode_code_parts()])
    assert a.md_content_no_yaml.rstrip() == from_parts.rstrip()

    # Test: save method
    a = hsg.Article(md_filename)
    a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
    a.md_content_no_yaml = "# New title\n\nNew content"
    a.save()
    new_content = Path(md_filename).read_text(encoding="utf8").lstrip()
    assert len(new_content.splitlines()) == 9
    Path(a.md_filename).write_text(TEST_MD_CONTENT, encoding="utf8")

    # Test: generate_html method creates index.html
    with TemporaryDirectory() as temp_dir:
        html_folder = Path(temp_dir) / "build_site"
        hsg.Article(md_filename).generate_html(html_folder)
        assert (html_folder / "index.html").is_file()

    # Test: html_code property returns HTML
    a = hsg.Article(md_filename)
    html_code = a.html_code
    assert html_code is not None
    assert len(html_code) > 0
    assert "<h1" in html_code or "<p>" in html_code

    # Test: html_folder property getter and setter
    a = hsg.Article(md_filename)
    assert a.html_folder is None
    a.html_folder = "./build_site"
    assert a.html_folder is not None
    assert "build_site" in str(a.html_folder)

    # Test: html_filename property
    a = hsg.Article(md_filename)
    a.html_folder = "./build_site"
    html_filename = a.html_filename
    assert html_filename is not None
    assert html_filename.name == "index.html"

    # Test: load method
    a = hsg.Article(md_filename)
    a.load("./tests/data/test_02/test_02.md")
    assert a.md_filename.name == "test_02.md"

    # Test: featured_image_filenames property
    a = hsg.Article(md_filename)
    featured_images = a.featured_image_filenames
    assert len(featured_images) == 1
    assert "featured-image.png" in featured_images

    # Test: md_yaml property with empty dict
    with TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)
        md_file = temp_path / "test_no_yaml.md"
        md_file.write_text("# Title\n\nContent", encoding="utf8")
        a = hsg.Article(md_file)
        assert a.md_yaml == ""

    # Test: md_yaml property with YAML
    a = hsg.Article(md_filename)
    md_yaml = a.md_yaml
    assert md_yaml.startswith("---")
    assert "date: 2022-09-18" in md_yaml

    # Test: md_yaml_dict property
    a = hsg.Article(md_filename)
    yaml_dict = a.md_yaml_dict
    assert isinstance(yaml_dict, dict)
    assert "date" in yaml_dict
    assert "categories" in yaml_dict
    assert "tags" in yaml_dict

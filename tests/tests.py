import datetime
import unittest
from pathlib import Path

import harrixpyssg as hsg

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


class TestHarrixpyssg(unittest.TestCase):
    def test_article__01(self):
        md_filename = "./tests/data/test_01/test_01.md"
        html_folder = "./build_site"
        hsg.Article(md_filename).generate_html(html_folder)
        self.assertTrue((Path(html_folder) / "index.html").is_file())

    def test_article__02(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        self.assertEqual(
            len(a.md_content.splitlines()), len(TEST_MD_CONTENT.splitlines())
        )

    def test_article__03(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        self.assertEqual(a.md_filename.name, "test_01.md")

    def test_article__04(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        a.md_content_no_yaml = "# New Title"
        self.assertEqual(len(a.md_content_no_yaml.splitlines()), 1)

    def test_article__05(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        len_yaml = len(a.md_yaml.splitlines())
        a.md_content_no_yaml = "# New Title"
        self.assertEqual(len(a.md_content.splitlines()), len_yaml + 2)

    def test_article__06(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        self.assertEqual(len(a.featured_image_filenames), 1)

    def test_article__07(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
        self.assertEqual(a.md_content.splitlines()[1], "date: 2022-11-04")

    def test_article__08(self):
        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        a.md_yaml_dict["categories"].append("test")
        self.assertEqual(a.md_content.splitlines()[2], "categories: [it, web, test]")

    def test_static_site_generator__01(self):
        md_folder = "./tests/data"
        html_folder = "./build_site"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(html_folder)
        count_files = 0
        for item in filter(
            lambda path: not any((part for part in path.parts if part.startswith("."))),
            Path(html_folder).rglob("*"),
        ):
            if item.is_file():
                count_files += 1
        self.assertEqual(count_files, 7)

    def test_static_site_generator__02(self):
        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        self.assertEqual(len(sg.articles), 3)


if __name__ == "__main__":
    unittest.main()

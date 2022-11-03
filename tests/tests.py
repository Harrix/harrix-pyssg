import unittest
from pathlib import Path

import harrixpyssg as hsg


class TestHarrixpyssg(unittest.TestCase):
    def test_article__01(self):
        md_filename = "./tests/data/test_01/test_01.md"
        html_folder = "./build_site"
        hsg.Article(md_filename).generate_html(html_folder)
        self.assertTrue((Path(html_folder) / "index.html").is_file())

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


if __name__ == "__main__":
    unittest.main()

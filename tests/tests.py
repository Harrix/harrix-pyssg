import unittest
from pathlib import Path

import harrixpyssg as hsg


class TestHarrixpyssg(unittest.TestCase):
    def test_article__01(self):
        md_filename = "./tests/data/test/test.md"
        html_folder = "./build_site"
        hsg.Article(md_filename).generate_html(html_folder)
        self.assertTrue((Path(html_folder) / "index.html").is_file())


if __name__ == "__main__":
    unittest.main()

"""
## Usage examples

```python
import harrixpyssg as hsg

md_folder = "C:/GitHub/harrix.dev/content"
html_folder = "C:/GitHub/harrix.dev/build_site"
sg = hsg.StaticSiteGenerator(md_folder)
sg.generate_site(html_folder)
```

```python
import harrixpyssg as hsg

md_folder = "./tests/data"
html_folder = "./build_site"
sg = hsg.StaticSiteGenerator(md_folder)
sg.generate_site(html_folder)
```

## Example of folder structure

Folder with the Markdown files:

```text
data
├─ test_01
│  ├─ featured-image.png
│  ├─ img
│  │  └─ test-image.png
│  └─ test_01.md
└─ test_02
   ├─ featured-image.png
   ├─ img
   │  └─ test-image.png
   └─ test_02.md
```

Output HTML folder:

```text
build_site
├─ test_01
│  ├─ featured-image.png
│  ├─ img
│  │  └─ test-image.png
│  └─ index.html
└─ test_02
   ├─ featured-image.png
   ├─ img
   │  └─ test-image.png
   └─ index.html
```
"""
from __future__ import annotations

import shutil
from pathlib import Path

from .article import Article
from .custom_logger import logger


class StaticSiteGenerator:
    """
    Static site generator. It collects Markdown files from folder and sub-folders.
    """

    def __init__(self, md_folder: str | Path):
        """
        The generator collects Markdown files from folder and sub-folders.
        Constructor `__init__` does not generate new files and folders.

        Attributes:

        - `md_folder` (str | Path): Folder with Markdown files. Example: `"./tests/data"`.
        - `articles` (list[Article]): list of all articles that is generated
        in the `__init__()`.
        - `html_folder` (str | Path): Output folder of HTML files.
        Example: `"./build_site"`.

        Example:

        ```python
        import harrixpyssg as hsg

        sg = hsg.StaticSiteGenerator("C:/GitHub/harrix.dev/content")
        ```
        """
        self._md_folder = Path(md_folder)
        self._articles: list[Article] = list()
        self.html_folder = Path()

        self.__get_info_about_articles()

    @property
    def md_folder(self):
        """
        `Path`: Folder with Markdown files (only getter).

        ```python
        import harrixpyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        print(sg.md_folder)
        # tests\data
        ```
        """
        return self._md_folder

    @property
    def articles(self):
        """
        `list[Article]`: list of all articles that is generated in the `__init__()`.

        ```python
        import harrixpyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        articles = sg.articles # list of all articles
        print(sg.articles[0].md_filename)
        # C:\GitHub\harrix-pyssg\tests\data\test_01\test_01.md
        ```
        """
        return self._articles

    def generate_site(self, html_folder: str | Path) -> StaticSiteGenerator:
        """
        This method generates HTML files with folders from the Markdown files.

        Args:

        - `html_folder` (str | Path): Output folder of the HTML files.

        Returns:

        - `Article`: Returns itself.
        """
        self.html_folder = Path(html_folder)

        self.__clear_html_folder_directory()

        for article in self.articles:
            parts = list(article.md_filename.parts[len(self.md_folder.parts) : -1])
            html_folder_article = self.html_folder / "/".join(parts)
            html_folder_article.mkdir(parents=True, exist_ok=True)
            article.generate_html(html_folder_article)

        return self

    def __get_info_about_articles(self):
        for item in filter(
            lambda path: not any((part for part in path.parts if part.startswith("."))),
            Path(self.md_folder).rglob("*"),
        ):
            if item.is_file() and item.suffix.lower() == ".md":
                self.articles.append(Article(item))

    def __clear_html_folder_directory(self) -> None:
        """
        This method clears `self.html_folder` with sub-directories.
        """
        shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)

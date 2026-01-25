"""Static site generator module for converting Markdown files to HTML."""

from __future__ import annotations

import shutil
from pathlib import Path

import harrix_pyssg as hsg


class StaticSiteGenerator:
    """Static site generator. It collects Markdown files from folder and sub-folders.

    ## Usage examples

    ```python
    import harrix_pyssg as hsg

    md_folder = "C:/GitHub/harrix.dev/content"
    html_folder = "C:/GitHub/harrix.dev/build_site"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.generate_site(html_folder)
    ```

    ```python
    import harrix_pyssg as hsg

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

    def __init__(self, md_folder: str | Path) -> None:
        """Collect Markdown files from folder and sub-folders.

        Constructor `__init__` does not generate new files and folders.

        Args:

        - `md_folder` (`str | Path`): Folder with Markdown files. Example: `"./tests/data"`.

        Example:

        ```python
        import harrix_pyssg as hsg

        sg = hsg.StaticSiteGenerator("C:/GitHub/harrix.dev/content")
        ```

        """
        self._md_folder = Path(md_folder)
        self._articles: list[hsg.Article] = []
        self._html_folder = None

        self._get_info_about_articles()

    @property
    def articles(self) -> list[hsg.Article]:
        r"""List of all articles that is generated in the `__init__()`.

        Returns:

        - `list[Article]`: List of all articles.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        articles = sg.articles  # list of all articles
        print(sg.articles[0].md_filename)
        # C:\\GitHub\\harrix-pyssg\tests\\data\test_01\test_01.md
        ```

        """
        return self._articles

    def generate_site(self, html_folder: str | Path | None = None) -> StaticSiteGenerator:
        """Generate HTML files with folders from Markdown files.

        Args:

        - `html_folder` (`str | Path | None`): Output folder of the HTML files. Defaults to `None`.

        Returns:

        - `StaticSiteGenerator`: Returns itself.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        html_folder = "./build_site"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(html_folder)
        ```

        """
        if html_folder is not None:
            self.html_folder = html_folder
        if self.html_folder is None:
            return self

        self._clear_html_folder_directory()

        for article in self.articles:
            parts = list(article.md_filename.parts[len(self.md_folder.parts) : -1])
            html_folder_article = self.html_folder / "/".join(parts)
            html_folder_article.mkdir(parents=True, exist_ok=True)
            article.generate_html(html_folder_article)

        return self

    def get_set_variables_from_yaml(self) -> list[str]:
        """Generate a sorted list of all variables from YAML from all articles.

        Returns:

        - `list[str]`: Sorted list of all variables from YAML from all articles.
          Example: `['categories', 'date', 'tags']`.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        print(sg.get_set_variables_from_yaml())
        # ['categories', 'date', 'tags']
        ```

        """
        res = set()
        for article in self.articles:
            for key in article.md_yaml_dict:
                res.add(key)
        return sorted(res)

    @property
    def html_folder(self) -> Path | None:
        r"""Output folder of HTML files.

        Returns:

        - `Path | None`: Output folder of HTML files.

        Example for the getter:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        html_folder = "./build_site"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(html_folder)
        print(sg.html_folder)
        # C:\\GitHub\\harrix-pyssg\build_site
        ```

        Example for the setter:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.html_folder = "./build_site"
        sg.generate_site()
        ```

        """
        if self._html_folder is not None:
            return self._html_folder.absolute()
        return None

    @html_folder.setter
    def html_folder(self, new_value: str | Path) -> None:
        self._html_folder = Path(new_value)

    @property
    def md_folder(self) -> Path:
        r"""Folder with Markdown files (only getter).

        Returns:

        - `Path`: Folder with Markdown files.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        print(sg.md_folder)
        # C:\\GitHub\\harrix-pyssg\tests\\data
        ```

        """
        return self._md_folder.absolute()

    def _clear_html_folder_directory(self) -> None:
        """Clear `self.html_folder` with sub-directories."""
        if self.html_folder is None:
            return
        if self.html_folder.exists() and self.html_folder.is_dir():
            shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)

    def _get_info_about_articles(self) -> None:
        """Get info from all Markdown files and fill the list `self.articles`."""
        for item in filter(
            lambda path: not any(part for part in path.parts if part.startswith(".")),
            Path(self.md_folder).rglob("*"),
        ):
            if item.is_file() and item.suffix.lower() == ".md":
                self.articles.append(hsg.Article(item))

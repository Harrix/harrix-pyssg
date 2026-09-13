"""Static site generator module for converting Markdown files to HTML."""

from __future__ import annotations

import shutil
from pathlib import Path

import harrix_pyssg as hsg
from harrix_pyssg.icon_catalog import IconFamily, load_icon_families, resolve_icons_repo_root
from harrix_pyssg.icon_pages import IconGridPage, collect_icon_grid_pages, icon_section_links, render_icon_grid_html
from harrix_pyssg.listing import ListingPage, collect_listing_pages, render_listing_html
from harrix_pyssg.page_assembler import PageAssembler, asset_prefix_for
from harrix_pyssg.site_layout import SiteSettings, build_catalog, place_article

_KEEP_HTML_FOLDER_NAMES = frozenset({".git", ".gitignore", ".gitattributes"})


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

    def __init__(
        self,
        md_folder: str | Path,
        theme_dir: str | Path | None = None,
        *,
        site_name: str = "harrix.dev",
        default_language: str = "ru",
        site_title: str = "Harrix",
        per_page: int = 20,
        icons_dir: str | Path | None = None,
        icons_per_page: int = 96,
        icons_language: str = "en",
    ) -> None:
        """Collect Markdown files from folder and sub-folders.

        Constructor `__init__` does not generate new files and folders.

        Args:

        - `md_folder` (`str | Path`): Folder with Markdown files. Example: `./tests/data`.
        - `theme_dir` (`str | Path | None`): Optional sliced theme directory. When set,
          generated pages are full HTML documents using theme chrome and assets.
        - `site_name` (`str`): Site host and content-repo prefix. Defaults to `harrix.dev`.
        - `default_language` (`str`): Language used when a repo has no `-en` suffix.
        - `site_title` (`str`): Title on the homepage and in listing `<title>` tags.
        - `per_page` (`int`): Articles per listing page. Defaults to `20`.
        - `icons_dir` (`str | Path | None`): Harrix-Vector-Icons repo root or `icons/` folder.
        - `icons_per_page` (`int`): Icons per catalog grid page. Defaults to `96`.
        - `icons_language` (`str`): Fallback language for icon URLs. Defaults to `en`.

        Example:

        ```python
        import harrix_pyssg as hsg

        sg = hsg.StaticSiteGenerator("C:/GitHub/harrix.dev/content")
        ```

        """
        self._md_folder = Path(md_folder)
        self._articles: list[hsg.Article] = []
        self._html_folder = None
        self._theme_dir = Path(theme_dir) if theme_dir is not None else None
        self._settings = SiteSettings(
            site_name=site_name,
            default_language=default_language,
            site_title=site_title,
            per_page=per_page,
            icons_per_page=icons_per_page,
            icons_language=icons_language,
        )
        self._icons_dir = Path(icons_dir) if icons_dir is not None else None
        self._listing_pages: list[ListingPage] = []
        self._icon_families: list[IconFamily] = []
        self._icon_grid_pages: list[IconGridPage] = []

        self._get_info_about_articles()

    @property
    def articles(self) -> list[hsg.Article]:
        r"""List of all articles that are generated in the `__init__()`.

        Returns:

        - `list[hsg.Article]`: List of all articles.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        articles = sg.articles  # list of all articles
        print(sg.articles[0].md_filename)
        # C:\\GitHub\\harrix-pyssg\\tests\\data\\test_01\\test_01.md
        ```

        """
        return self._articles

    def generate_site(
        self,
        html_folder: str | Path | None = None,
        theme_dir: str | Path | None = None,
    ) -> StaticSiteGenerator:
        """Generate HTML files with folders from Markdown files.

        Args:

        - `html_folder` (`str | Path | None`): Output folder of the HTML files. Defaults to `None`.
        - `theme_dir` (`str | Path | None`): Optional sliced theme directory. Overrides the
          theme passed to the constructor when set.

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
        if theme_dir is not None:
            self._theme_dir = Path(theme_dir)
        if self.html_folder is None:
            return self

        self._clear_html_folder_directory()

        assembler = None
        if self._theme_dir is not None:
            assembler = PageAssembler(self._theme_dir)
            assembler.copy_assets_to(self.html_folder)

        catalog = build_catalog(self.articles, self.md_folder, self._settings)
        published = {id(entry.article) for entry in catalog}

        for article in self.articles:
            if id(article) not in published:
                continue
            placement = place_article(article, self.md_folder, self._settings)
            html_folder_article = self.html_folder / placement.rel_output
            html_folder_article.mkdir(parents=True, exist_ok=True)
            article.generate_html(
                html_folder_article,
                page_assembler=assembler,
                site_root=self.html_folder if assembler is not None else None,
            )

        self._icon_families = []
        if self._icons_dir is not None:
            self._icon_families = load_icon_families(
                self._icons_dir,
                default_lang=self._settings.icons_language,
            )
            self._generate_icon_family_pages(assembler)

        extra_links = icon_section_links(self._icon_families, self._settings)
        self._listing_pages = collect_listing_pages(catalog, self._settings, extra_links)
        for listing in self._listing_pages:
            self._write_listing_page(listing, assembler)

        self._icon_grid_pages = collect_icon_grid_pages(self._icon_families, self._settings)
        for grid in self._icon_grid_pages:
            self._write_icon_grid_page(grid, assembler)

        return self

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
        # C:\\GitHub\\harrix-pyssg\\build_site
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
    def icon_families(self) -> list[IconFamily]:
        """Icon families loaded during the last `generate_site()` call."""
        return self._icon_families

    @property
    def icon_grid_pages(self) -> list[IconGridPage]:
        """Icon catalog grid pages created by the last `generate_site()` call."""
        return self._icon_grid_pages

    @property
    def listing_pages(self) -> list[ListingPage]:
        """Listing pages created by the last `generate_site()` call.

        Returns:

        - `list[ListingPage]`: Homepage, section, year, and taxonomy pages.

        """
        return self._listing_pages

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
        # C:\\GitHub\\harrix-pyssg\\tests\\data
        ```

        """
        return self._md_folder.absolute()

    @property
    def settings(self) -> SiteSettings:
        """Site settings used for URLs, language, and pagination."""
        return self._settings

    @property
    def theme_dir(self) -> Path | None:
        """Sliced theme directory used for full-page generation.

        Returns:

        - `Path | None`: Theme directory, or `None` when generating HTML fragments only.

        """
        return self._theme_dir.resolve() if self._theme_dir is not None else None

    def _clear_html_folder_directory(self) -> None:
        """Clear generated files in `self.html_folder`, keeping Git metadata.

        Removes every child except `.git`, `.gitignore`, and `.gitattributes` so a
        deploy repository in the HTML output folder survives regeneration.

        """
        if self.html_folder is None:
            return
        self.html_folder.mkdir(parents=True, exist_ok=True)
        for child in self.html_folder.iterdir():
            if child.name in _KEEP_HTML_FOLDER_NAMES:
                continue
            if child.is_dir() and not child.is_symlink():
                shutil.rmtree(child)
            else:
                child.unlink()

    def _generate_icon_family_pages(self, assembler: PageAssembler | None) -> None:
        """Write one themed page per icon note and copy featured SVG files."""
        if self.html_folder is None or self._icons_dir is None:
            return
        repo_root = resolve_icons_repo_root(self._icons_dir)
        for family in self._icon_families:
            dest = self.html_folder / family.rel_output
            dest.mkdir(parents=True, exist_ok=True)
            note = family.note_path(repo_root)
            if note is not None:
                article = hsg.Article(note)
                article.generate_html(
                    dest,
                    page_assembler=assembler,
                    site_root=self.html_folder if assembler is not None else None,
                )
                continue
            featured = family.featured_path(repo_root)
            if featured is not None:
                shutil.copy2(featured, dest / featured.name)

    def _get_info_about_articles(self) -> None:
        """Get info from all Markdown files and fill the list `self.articles`."""
        for item in filter(
            lambda path: not any(part for part in path.parts if part.startswith(".")),
            Path(self.md_folder).rglob("*"),
        ):
            if item.is_file() and item.suffix.lower() == ".md":
                self.articles.append(hsg.Article(item))

    def _write_icon_grid_page(self, grid: IconGridPage, assembler: PageAssembler | None) -> None:
        """Write one icon-grid `index.html` without clearing family folders."""
        if self.html_folder is None:
            return
        page_dir = self.html_folder / grid.rel_dir
        page_dir.mkdir(parents=True, exist_ok=True)
        content_html = render_icon_grid_html(grid)
        if assembler is not None:
            prefix = asset_prefix_for(page_dir, self.html_folder)
            html = assembler.assemble(
                content_html=content_html,
                title=grid.title,
                asset_prefix=prefix,
            )
        else:
            html = content_html
        (page_dir / "index.html").write_text(html, encoding="utf8")

    def _write_listing_page(self, listing: ListingPage, assembler: PageAssembler | None) -> None:
        """Write one listing `index.html` without clearing sibling article folders."""
        if self.html_folder is None:
            return
        page_dir = self.html_folder / listing.rel_dir
        page_dir.mkdir(parents=True, exist_ok=True)
        content_html = render_listing_html(listing)
        if assembler is not None:
            prefix = asset_prefix_for(page_dir, self.html_folder)
            html = assembler.assemble(
                content_html=content_html,
                title=listing.title,
                asset_prefix=prefix,
            )
        else:
            html = content_html
        (page_dir / "index.html").write_text(html, encoding="utf8")

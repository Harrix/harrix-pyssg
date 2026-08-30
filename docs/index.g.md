---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# Harrix PySSG

![Featured image](https://raw.githubusercontent.com/Harrix/harrix-pyssg/refs/heads/main/img/featured-image.svg)

🔌 Simple static site generator in Python. **In development**.

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🛠️ Technologies](#%EF%B8%8F-technologies)
- [📦 Installation](#-installation)
- [📚 List of functions](#-list-of-functions)
  - [📄 File `article.py`](#-file-articlepy)
  - [📄 File `icon_catalog.py`](#-file-icon_catalogpy)
  - [📄 File `icon_pages.py`](#-file-icon_pagespy)
  - [📄 File `listing.py`](#-file-listingpy)
  - [📄 File `marp_render.py`](#-file-marp_renderpy)
  - [📄 File `page_assembler.py`](#-file-page_assemblerpy)
  - [📄 File `site_layout.py`](#-file-site_layoutpy)
  - [📄 File `static_site_generator.py`](#-file-static_site_generatorpy)
  - [📄 File `theme_slicer.py`](#-file-theme_slicerpy)
- [📄 License](#-license)
- [👤 Author](#-author)

</details>

![GitHub](https://img.shields.io/badge/GitHub-harrix--pyssg-blue?logo=github) ![GitHub](https://img.shields.io/github/license/Harrix/harrix-pyssg) ![PyPI](https://img.shields.io/pypi/v/harrix-pyssg)

GitHub: <https://github.com/Harrix/harrix-pyssg>

Documentation: [docs](https://github.com/Harrix/harrix-pyssg/blob/main/docs/index.g.md)

## 🛠️ Technologies

Markdown processor: [markdown-it-py](https://pypi.org/project/markdown-it-py) <https://pypistats.org/packages/markdown-it-py>.

Note title and date helpers (`resolve_note_title`, `resolve_note_date`, `title_from_id`) live in
[`harrix-pylib` `note_meta`](https://github.com/Harrix/harrix-pylib/blob/main/docs/note_meta.g.md)
and are re-exported from `harrix_pyssg.note_meta`.

## 📦 Installation

Using `pip`:

```shell
pip install harrix-pyssg
```

Using `uv` (recommended):

```shell
uv add harrix-pyssg
```

## 📚 List of functions

### 📄 File `article.py`

Doc: [article.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/article.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`Article`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/article.g.md#%EF%B8%8F-class-article) | All information about one article from the site. |

### 📄 File `icon_catalog.py`

Doc: [icon_catalog.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_catalog.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`IconFamily`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_catalog.g.md#%EF%B8%8F-class-iconfamily) | One icon family (note folder with a featured image and variants). |
| 🔧 [`load_icon_families`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_catalog.g.md#-function-load_icon_families) | Load icon families from a repo root or an `icons/` folder. |
| 🔧 [`resolve_icons_repo_root`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_catalog.g.md#-function-resolve_icons_repo_root) | Normalize a repo root or `icons/` folder to the repository root. |

### 📄 File `icon_pages.py`

Doc: [icon_pages.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_pages.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`IconGridPage`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_pages.g.md#%EF%B8%8F-class-icongridpage) | One generated icon-grid listing page. |
| 🔧 [`collect_icon_grid_pages`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_pages.g.md#-function-collect_icon_grid_pages) | Build all-icons and per-category grid pages (with pagination). |
| 🔧 [`icon_section_links`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_pages.g.md#-function-icon_section_links) | Homepage section buttons that open the icon catalog. |
| 🔧 [`render_icon_grid_html`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/icon_pages.g.md#-function-render_icon_grid_html) | Render an Icons8-style icon grid (body HTML only). |

### 📄 File `listing.py`

Doc: [listing.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/listing.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`ListingPage`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/listing.g.md#%EF%B8%8F-class-listingpage) | One generated listing page (a directory with `index.html`). |
| 🔧 [`collect_listing_pages`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/listing.g.md#-function-collect_listing_pages) | Build homepage, language, section, year, category, and tag listing pages. |
| 🔧 [`listing_rel_dir`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/listing.g.md#-function-listing_rel_dir) | Return the output directory for listing page number `page_num`. |
| 🔧 [`paginate`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/listing.g.md#-function-paginate) | Split catalog entries into pages of `per_page` items (at least one page). |
| 🔧 [`render_listing_html`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/listing.g.md#-function-render_listing_html) | Render listing body HTML for one page (without theme chrome). |

### 📄 File `marp_render.py`

Doc: [marp_render.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/marp_render.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🔧 [`is_marp_yaml`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/marp_render.g.md#-function-is_marp_yaml) | Return `True` when YAML enables a Marp presentation note. |
| 🔧 [`render_marp_html`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/marp_render.g.md#-function-render_marp_html) | Return a full HTML document for a Marp note. |

### 📄 File `page_assembler.py`

Doc: [page_assembler.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`PageAssembler`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#%EF%B8%8F-class-pageassembler) | Build a full HTML page from theme parts and article body HTML. |
| 🏛️ Class [`PageFeatures`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#%EF%B8%8F-class-pagefeatures) | Optional page features detected from Markdown/HTML/YAML. |
| 🔧 [`asset_prefix_for`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-asset_prefix_for) | Build a relative prefix from a page directory to the site root. |
| 🔧 [`detect_page_features`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-detect_page_features) | Detect optional features from rendered HTML, Markdown, and YAML. |
| 🔧 [`extract_title`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-extract_title) | Extract plain-text title from the first `<h1>` in HTML. |
| 🔧 [`rewrite_asset_paths`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-rewrite_asset_paths) | Prefix theme asset `href`/`src` values with `asset_prefix`. |

### 📄 File `site_layout.py`

Doc: [site_layout.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`ArticlePlacement`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#%EF%B8%8F-class-articleplacement) | Where one article lives on the generated site. |
| 🏛️ Class [`CatalogEntry`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#%EF%B8%8F-class-catalogentry) | Published article ready for listing pages. |
| 🏛️ Class [`SiteSettings`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#%EF%B8%8F-class-sitesettings) | Site-wide defaults used when placing articles and building listings. |
| 🔧 [`as_string_list`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-as_string_list) | Normalize a YAML list or scalar into a list of non-empty strings. |
| 🔧 [`build_catalog`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-build_catalog) | Build a newest-first catalog of published articles. |
| 🔧 [`excerpt_from_markdown`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-excerpt_from_markdown) | Take the first prose paragraph from Markdown as a short excerpt. |
| 🔧 [`is_published`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-is_published) | Return `False` only when YAML explicitly sets `published: false`. |
| 🔧 [`parse_content_repo_name`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-parse_content_repo_name) | Parse `{site}-{section}[-{year}][-{lang}]` into placement without a slug. |
| 🔧 [`path_to_url`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-path_to_url) | Turn a relative output directory into a site-absolute folder URL. |
| 🔧 [`place_article`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-place_article) | Resolve the output directory and URL parts for one article. |
| 🔧 [`section_label`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-section_label) | Localized label for a content section (`articles`, `games`, …). |
| 🔧 [`slugify_term`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-slugify_term) | Make a URL segment from a category or tag. |
| 🔧 [`ui_string`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/site_layout.g.md#-function-ui_string) | Return a listing UI string for `lang`, falling back to English. |

### 📄 File `static_site_generator.py`

Doc: [static_site_generator.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/static_site_generator.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`StaticSiteGenerator`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/static_site_generator.g.md#%EF%B8%8F-class-staticsitegenerator) | Static site generator. It collects Markdown files from folder and sub-folders. |

### 📄 File `theme_slicer.py`

Doc: [theme_slicer.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/theme_slicer.g.md)

| Function/Class | Description |
|----------------|-------------|
| 🏛️ Class [`ThemeSlicer`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/theme_slicer.g.md#%EF%B8%8F-class-themeslicer) | Cut a built HTML template page into reusable theme parts and assets. |

## 📄 License

This project is licensed under the [MIT License](https://github.com/Harrix/harrix-pyssg/blob/main/LICENSE.md).

## 👤 Author

Author: [Anton Sergienko](https://github.com/Harrix).

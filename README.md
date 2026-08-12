# Harrix PySSG

![Featured image](https://raw.githubusercontent.com/Harrix/harrix-pyssg/refs/heads/main/img/featured-image.svg)

🔌 Simple static site generator in Python. **In development**.

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🛠️ Technologies](#️-technologies)
- [📦 Installation](#-installation)
- [📚 List of functions](#-list-of-functions)
  - [📄 File `article.py`](#-file-articlepy)
  - [📄 File `note_meta.py`](#-file-note_metapy)
  - [📄 File `page_assembler.py`](#-file-page_assemblerpy)
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

Doc: [`article.g.md`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/article.g.md)

| Function/Class                                                                                          | Description                                      |
| ------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 🏛️ Class [`Article`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/article.g.md#️-class-article) | All information about one article from the site. |

### 📄 File `note_meta.py`

Doc: [`note_meta.g.md`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md)

| Function/Class                                                                                                                                 | Description                                                                         |
| ---------------------------------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------- |
| 🏛️ Class [`ResolvedNoteDate`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#️-class-resolvednotedate)                    | Resolved calendar date for a note and where it came from.                           |
| 🔧 [`extract_title_from_markdown`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-extract_title_from_markdown) | Return YAML `title` or first H1 from Markdown (empty when neither exists).          |
| 🔧 [`note_stem_from_name`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-note_stem_from_name)                 | Return file stem for `.md` / `.g.md` names.                                         |
| 🔧 [`parse_date_from_file_name`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-parse_date_from_file_name)     | Extract the first calendar date fragment from a file name / stem.                   |
| 🔧 [`parse_date_from_yaml`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-parse_date_from_yaml)               | Parse YAML frontmatter `date:` when present.                                        |
| 🔧 [`parse_date_value`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-parse_date_value)                       | Parse a YAML/scalar date value into a `date`.                                       |
| 🔧 [`resolve_note_date`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-resolve_note_date)                     | Resolve note date: file name → YAML `date` → ctime → mtime.                         |
| 🔧 [`resolve_note_date_for_path`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-resolve_note_date_for_path)   | Resolve note date for a filesystem path (reads the file when `md_text` is omitted). |
| 🔧 [`resolve_note_title`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/note_meta.g.md#-function-resolve_note_title)                   | Resolve display title: YAML `title` → H1 → `file_stem`.                             |

### 📄 File `page_assembler.py`

Doc: [`page_assembler.g.md`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md)

| Function/Class                                                                                                                        | Description                                                      |
| ------------------------------------------------------------------------------------------------------------------------------------- | ---------------------------------------------------------------- |
| 🏛️ Class [`PageAssembler`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#️-class-pageassembler)            | Build a full HTML page from theme parts and article body HTML.   |
| 🏛️ Class [`PageFeatures`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#️-class-pagefeatures)              | Optional page features detected from Markdown/HTML/YAML.         |
| 🔧 [`asset_prefix_for`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-asset_prefix_for)         | Build a relative prefix from a page directory to the site root.  |
| 🔧 [`detect_page_features`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-detect_page_features) | Detect optional features from rendered HTML, Markdown, and YAML. |
| 🔧 [`extract_title`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-extract_title)               | Extract plain-text title from the first `<h1>` in HTML.          |
| 🔧 [`rewrite_asset_paths`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/page_assembler.g.md#-function-rewrite_asset_paths)   | Prefix theme asset `href`/`src` values with `asset_prefix`.      |

### 📄 File `static_site_generator.py`

Doc: [`static_site_generator.g.md`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/static_site_generator.g.md)

| Function/Class                                                                                                                                | Description                                                                    |
| --------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| 🏛️ Class [`StaticSiteGenerator`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/static_site_generator.g.md#️-class-staticsitegenerator) | Static site generator. It collects Markdown files from folder and sub-folders. |

### 📄 File `theme_slicer.py`

Doc: [`theme_slicer.g.md`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/theme_slicer.g.md)

| Function/Class                                                                                                       | Description                                                          |
| -------------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------- |
| 🏛️ Class [`ThemeSlicer`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/theme_slicer.g.md#️-class-themeslicer) | Cut a built HTML template page into reusable theme parts and assets. |

## 📄 License

This project is licensed under the [MIT License](https://github.com/Harrix/harrix-pyssg/blob/main/LICENSE.md).

## 👤 Author

Author: [Anton Sergienko](https://github.com/Harrix).

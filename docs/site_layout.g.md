---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# 📄 File `site_layout.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🏛️ Class `ArticlePlacement`](#%EF%B8%8F-class-articleplacement)
- [🏛️ Class `CatalogEntry`](#%EF%B8%8F-class-catalogentry)
  - [⚙️ Method `featured_image_url (property)`](#%EF%B8%8F-method-featured_image_url-property)
  - [⚙️ Method `url (property)`](#%EF%B8%8F-method-url-property)
- [🏛️ Class `SiteSettings`](#%EF%B8%8F-class-sitesettings)
- [🔧 Function `as_string_list`](#-function-as_string_list)
- [🔧 Function `build_catalog`](#-function-build_catalog)
- [🔧 Function `excerpt_from_markdown`](#-function-excerpt_from_markdown)
- [🔧 Function `is_published`](#-function-is_published)
- [🔧 Function `parse_content_repo_name`](#-function-parse_content_repo_name)
- [🔧 Function `path_to_url`](#-function-path_to_url)
- [🔧 Function `place_article`](#-function-place_article)
- [🔧 Function `section_label`](#-function-section_label)
- [🔧 Function `slugify_term`](#-function-slugify_term)
- [🔧 Function `ui_string`](#-function-ui_string)

</details>

## 🏛️ Class `ArticlePlacement`

```python
class ArticlePlacement
```

Where one article lives on the generated site.

<details>
<summary>Code:</summary>

```python
class ArticlePlacement:

    lang: str
    slug: str
    rel_output: Path
    section: str | None = None
    year: str | None = None
```

</details>

## 🏛️ Class `CatalogEntry`

```python
class CatalogEntry
```

Published article ready for listing pages.

<details>
<summary>Code:</summary>

```python
class CatalogEntry:

    article: Article
    placement: ArticlePlacement
    title: str
    date: datetime.date | None
    excerpt: str
    featured_image: str | None
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)

    @property
    def featured_image_url(self) -> str | None:
        """Site-absolute URL of the featured image, if any."""
        if not self.featured_image:
            return None
        return f"{self.url}{self.featured_image}"

    @property
    def url(self) -> str:
        """Site-absolute URL of the article folder (`/ru/articles/2013/slug/`)."""
        return path_to_url(self.placement.rel_output)
```

</details>

### ⚙️ Method `featured_image_url (property)`

```python
def featured_image_url(self) -> str | None
```

Site-absolute URL of the featured image, if any.

<details>
<summary>Code:</summary>

```python
def featured_image_url(self) -> str | None:
        if not self.featured_image:
            return None
        return f"{self.url}{self.featured_image}"
```

</details>

### ⚙️ Method `url (property)`

```python
def url(self) -> str
```

Site-absolute URL of the article folder (`/ru/articles/2013/slug/`).

<details>
<summary>Code:</summary>

```python
def url(self) -> str:
        return path_to_url(self.placement.rel_output)
```

</details>

## 🏛️ Class `SiteSettings`

```python
class SiteSettings
```

Site-wide defaults used when placing articles and building listings.

<details>
<summary>Code:</summary>

```python
class SiteSettings:

    site_name: str = "harrix.dev"
    default_language: str = "ru"
    site_title: str = "Harrix"
    per_page: int = 20
    icons_per_page: int = 96
    icons_language: str = "en"
```

</details>

## 🔧 Function `as_string_list`

```python
def as_string_list(value: Any) -> list[str]
```

Normalize a YAML list or scalar into a list of non-empty strings.

<details>
<summary>Code:</summary>

```python
def as_string_list(value: Any) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        item = value.strip()
        return [item] if item else []
    if isinstance(value, list):
        result: list[str] = []
        for item in value:
            text = str(item).strip()
            if text:
                result.append(text)
        return result
    return []
```

</details>

## 🔧 Function `build_catalog`

```python
def build_catalog(articles: list[Article], md_folder: Path, settings: SiteSettings) -> list[CatalogEntry]
```

Build a newest-first catalog of published articles.

<details>
<summary>Code:</summary>

```python
def build_catalog(articles: list[Article], md_folder: Path, settings: SiteSettings) -> list[CatalogEntry]:
    catalog: list[CatalogEntry] = []
    for article in articles:
        if not is_published(article.md_yaml_dict):
            continue
        placement = place_article(article, md_folder, settings)
        featured = article.featured_image_filenames
        catalog.append(
            CatalogEntry(
                article=article,
                placement=placement,
                title=resolve_note_title(article.md_content, file_stem=article.md_filename.stem),
                date=_article_date(article),
                excerpt=excerpt_from_markdown(article.md_content_no_yaml),
                featured_image=featured[0] if featured else None,
                categories=as_string_list(article.md_yaml_dict.get("categories")),
                tags=as_string_list(article.md_yaml_dict.get("tags")),
            )
        )
    catalog.sort(key=_catalog_sort_key)
    return catalog
```

</details>

## 🔧 Function `excerpt_from_markdown`

```python
def excerpt_from_markdown(md_content: str, limit: int = _EXCERPT_LIMIT) -> str
```

Take the first prose paragraph from Markdown as a short excerpt.

<details>
<summary>Code:</summary>

```python
def excerpt_from_markdown(md_content: str, limit: int = _EXCERPT_LIMIT) -> str:
    chunks: list[str] = []
    for raw_line in md_content.splitlines():
        line = raw_line.strip()
        if not line:
            if chunks:
                break
            continue
        if line.startswith(_MD_SKIP_PREFIXES):
            continue
        chunks.append(line)

    text = " ".join(chunks)
    text = _MD_IMAGE_RE.sub("", text)
    text = _MD_LINK_RE.sub(r"\1", text)
    text = _MD_EMPHASIS_RE.sub("", text)
    text = " ".join(text.split()).strip()
    if len(text) <= limit:
        return text
    return text[: limit - 1].rstrip() + "…"
```

</details>

## 🔧 Function `is_published`

```python
def is_published(yaml_dict: dict[str, Any] | None) -> bool
```

Return `False` only when YAML explicitly sets `published: false`.

<details>
<summary>Code:</summary>

```python
def is_published(yaml_dict: dict[str, Any] | None) -> bool:
    if not yaml_dict:
        return True
    return yaml_dict.get("published", True) is not False
```

</details>

## 🔧 Function `parse_content_repo_name`

```python
def parse_content_repo_name(repo_name: str, settings: SiteSettings) -> ArticlePlacement | None
```

Parse `{site}-{section}[-{year}][-{lang}]` into placement without a slug.

<details>
<summary>Code:</summary>

```python
def parse_content_repo_name(repo_name: str, settings: SiteSettings) -> ArticlePlacement | None:
    prefix = f"{settings.site_name}-"
    if not repo_name.startswith(prefix):
        return None
    tokens = [token for token in repo_name[len(prefix) :].split("-") if token]
    if not tokens:
        return None
    lang = settings.default_language
    year: str | None = None
    if len(tokens) >= _MIN_REPO_TAIL_PARTS and _LANG_RE.fullmatch(tokens[-1]):
        lang = tokens.pop().lower()
    if tokens and _YEAR_RE.fullmatch(tokens[-1]):
        year = tokens.pop()
    section = "-".join(tokens)
    if not section:
        return None
    return ArticlePlacement(lang=lang, slug="", rel_output=Path(), section=section, year=year)
```

</details>

## 🔧 Function `path_to_url`

```python
def path_to_url(rel_dir: Path | str) -> str
```

Turn a relative output directory into a site-absolute folder URL.

<details>
<summary>Code:</summary>

```python
def path_to_url(rel_dir: Path | str) -> str:
    text = rel_dir.as_posix() if isinstance(rel_dir, Path) else str(rel_dir).replace("\\", "/")
    text = text.strip("/")
    return f"/{text}/" if text else "/"
```

</details>

## 🔧 Function `place_article`

```python
def place_article(article: Article, md_folder: Path, settings: SiteSettings) -> ArticlePlacement
```

Resolve the output directory and URL parts for one article.

Supports:

- content-repo root: `{site}-{section}[-year][-lang]/{slug}/{slug}.md`
- site-repo tree: `{lang}/{section}/[{year}/]{slug}/{slug}.md`
- flat folders: keep the relative parent path of the Markdown file

<details>
<summary>Code:</summary>

```python
def place_article(article: Article, md_folder: Path, settings: SiteSettings) -> ArticlePlacement:
    rel = article.md_filename.resolve().relative_to(Path(md_folder).resolve())
    parts = list(rel.parts)
    slug = article.md_filename.parent.name if len(parts) >= _ARTICLE_FOLDER_MIN_PARTS else article.md_filename.stem
    yaml_lang = str(article.md_yaml_dict.get("lang") or "").strip().lower()
    lang = yaml_lang if _LANG_RE.fullmatch(yaml_lang) else settings.default_language

    if parts:
        parsed = parse_content_repo_name(parts[0], settings)
        if parsed is not None and parsed.section is not None:
            rel_output = _article_rel_output(parsed.lang, parsed.section, parsed.year, slug)
            return ArticlePlacement(
                lang=parsed.lang,
                slug=slug,
                rel_output=rel_output,
                section=parsed.section,
                year=parsed.year,
            )

    if len(parts) >= _SITE_TREE_MIN_PARTS and _LANG_RE.fullmatch(parts[0]):
        lang = parts[0].lower()
        section = parts[1]
        year = parts[2] if len(parts) >= _SITE_TREE_WITH_YEAR_PARTS and _YEAR_RE.fullmatch(parts[2]) else None
        rel_output = _article_rel_output(lang, section, year, slug)
        return ArticlePlacement(lang=lang, slug=slug, rel_output=rel_output, section=section, year=year)

    rel_output = Path(*parts[:-1]) if len(parts) >= _ARTICLE_FOLDER_MIN_PARTS else Path(slug)
    return ArticlePlacement(lang=lang, slug=slug, rel_output=rel_output)
```

</details>

## 🔧 Function `section_label`

```python
def section_label(section: str, lang: str) -> str
```

Localized label for a content section ([`articles`](static_site_generator.g.md#%EF%B8%8F-method-articles-property), `games`, …).

<details>
<summary>Code:</summary>

```python
def section_label(section: str, lang: str) -> str:
    labels = SECTION_LABELS.get(section)
    if labels:
        return labels.get(lang) or labels.get("en") or section
    return section.replace("-", " ").capitalize()
```

</details>

## 🔧 Function `slugify_term`

```python
def slugify_term(value: str) -> str
```

Make a URL segment from a category or tag.

<details>
<summary>Code:</summary>

```python
def slugify_term(value: str) -> str:
    text = value.strip()
    if _SAFE_SLUG_RE.fullmatch(text):
        return text
    return quote(text.replace(" ", "-"), safe="-_.")
```

</details>

## 🔧 Function `ui_string`

```python
def ui_string(lang: str, key: str) -> str
```

Return a listing UI string for `lang`, falling back to English.

<details>
<summary>Code:</summary>

```python
def ui_string(lang: str, key: str) -> str:
    table = UI_STRINGS.get(lang) or UI_STRINGS["en"]
    return table.get(key) or UI_STRINGS["en"].get(key, key)
```

</details>

---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# 📄 File `listing.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🏛️ Class `ListingPage`](#%EF%B8%8F-class-listingpage)
- [🔧 Function `collect_listing_pages`](#-function-collect_listing_pages)
- [🔧 Function `listing_rel_dir`](#-function-listing_rel_dir)
- [🔧 Function `paginate`](#-function-paginate)
- [🔧 Function `render_listing_html`](#-function-render_listing_html)

</details>

## 🏛️ Class `ListingPage`

```python
class ListingPage
```

One generated listing page (a directory with `index.html`).

<details>
<summary>Code:</summary>

```python
class ListingPage:

    rel_dir: Path
    title: str
    lang: str
    heading: str
    entries: tuple[CatalogEntry, ...]
    page_num: int
    page_count: int
    page_base: Path
    crumbs: tuple[tuple[str, str], ...]
    section_links: tuple[tuple[str, str], ...]
    year_links: tuple[tuple[str, str], ...]
```

</details>

## 🔧 Function `collect_listing_pages`

```python
def collect_listing_pages(catalog: list[CatalogEntry], settings: SiteSettings, extra_section_links: tuple[tuple[str, str], ...] = ()) -> list[ListingPage]
```

Build homepage, language, section, year, category, and tag listing pages.

<details>
<summary>Code:</summary>

```python
def collect_listing_pages(
    catalog: list[CatalogEntry],
    settings: SiteSettings,
    extra_section_links: tuple[tuple[str, str], ...] = (),
) -> list[ListingPage]:
    pages: list[ListingPage] = []
    languages = sorted({entry.placement.lang for entry in catalog}) or [settings.default_language]
    site_mode = any(entry.placement.section for entry in catalog)

    if not site_mode:
        pages.extend(
            _paged_listings(
                entries=catalog,
                page_base=Path(),
                lang=settings.default_language,
                heading=settings.site_title,
                title=settings.site_title,
                crumbs=((ui_string(settings.default_language, "home"), "/"),),
                section_links=extra_section_links,
                year_links=(),
                settings=settings,
            )
        )
        return pages

    default_lang = settings.default_language if settings.default_language in languages else languages[0]
    default_home = _language_home_pages(catalog, default_lang, settings, extra_section_links)
    pages.extend(default_home)
    for copy_page in default_home:
        if copy_page.rel_dir == Path(default_lang) or copy_page.rel_dir.parts[:1] == (default_lang,):
            root_dir = Path(*copy_page.rel_dir.parts[1:])
            pages.append(
                ListingPage(
                    rel_dir=root_dir,
                    title=copy_page.title,
                    lang=copy_page.lang,
                    heading=copy_page.heading,
                    entries=copy_page.entries,
                    page_num=copy_page.page_num,
                    page_count=copy_page.page_count,
                    page_base=Path(*copy_page.page_base.parts[1:]),
                    crumbs=copy_page.crumbs,
                    section_links=copy_page.section_links,
                    year_links=copy_page.year_links,
                )
            )

    for lang in languages:
        if lang != default_lang:
            pages.extend(_language_home_pages(catalog, lang, settings, extra_section_links))
        pages.extend(_section_and_taxonomy_pages(catalog, lang, settings))
    return pages
```

</details>

## 🔧 Function `listing_rel_dir`

```python
def listing_rel_dir(page_base: Path, page_num: int) -> Path
```

Return the output directory for listing page number `page_num`.

<details>
<summary>Code:</summary>

```python
def listing_rel_dir(page_base: Path, page_num: int) -> Path:
    if page_num <= 1:
        return page_base
    return page_base / "page" / str(page_num)
```

</details>

## 🔧 Function `paginate`

```python
def paginate(items: list[CatalogEntry], per_page: int) -> list[list[CatalogEntry]]
```

Split catalog entries into pages of `per_page` items (at least one page).

<details>
<summary>Code:</summary>

```python
def paginate(items: list[CatalogEntry], per_page: int) -> list[list[CatalogEntry]]:
    size = max(1, per_page)
    if not items:
        return [[]]
    return [items[index : index + size] for index in range(0, len(items), size)]
```

</details>

## 🔧 Function `render_listing_html`

```python
def render_listing_html(page: ListingPage) -> str
```

Render listing body HTML for one page (without theme chrome).

<details>
<summary>Code:</summary>

```python
def render_listing_html(page: ListingPage) -> str:
    lang = page.lang
    parts = [
        _breadcrumb(page),
        f'<header>\n<h1 class="title">{html.escape(page.heading)}</h1>\n</header>\n',
    ]
    if page.section_links:
        parts.append(_link_row(ui_string(lang, "sections"), page.section_links))
    if page.year_links:
        parts.append(_link_row(ui_string(lang, "years"), page.year_links))
    if not page.entries:
        parts.append(f"<p>{html.escape(ui_string(lang, 'empty'))}</p>\n")
    else:
        parts.append(_post_list(page.entries, lang))
        parts.append(_pagination(page, lang))
    return "".join(parts)
```

</details>

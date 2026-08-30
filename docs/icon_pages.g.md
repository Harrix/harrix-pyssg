---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# 📄 File `icon_pages.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🏛️ Class `IconGridPage`](#%EF%B8%8F-class-icongridpage)
- [🔧 Function `collect_icon_grid_pages`](#-function-collect_icon_grid_pages)
- [🔧 Function `icon_section_links`](#-function-icon_section_links)
- [🔧 Function `render_icon_grid_html`](#-function-render_icon_grid_html)

</details>

## 🏛️ Class `IconGridPage`

```python
class IconGridPage
```

One generated icon-grid listing page.

<details>
<summary>Code:</summary>

```python
class IconGridPage:

    rel_dir: Path
    title: str
    lang: str
    heading: str
    families: tuple[IconFamily, ...]
    page_num: int
    page_count: int
    page_base: Path
    crumbs: tuple[tuple[str, str], ...]
    category_links: tuple[tuple[str, str], ...]
```

</details>

## 🔧 Function `collect_icon_grid_pages`

```python
def collect_icon_grid_pages(families: list[IconFamily], settings: SiteSettings) -> list[IconGridPage]
```

Build all-icons and per-category grid pages (with pagination).

<details>
<summary>Code:</summary>

```python
def collect_icon_grid_pages(families: list[IconFamily], settings: SiteSettings) -> list[IconGridPage]:
    if not families:
        return []
    pages: list[IconGridPage] = []
    languages = sorted({family.lang for family in families})
    for lang in languages:
        lang_families = [family for family in families if family.lang == lang]
        pages.extend(_grids_for_language(lang_families, lang, settings))
    return pages
```

</details>

## 🔧 Function `icon_section_links`

```python
def icon_section_links(families: list[IconFamily], settings: SiteSettings) -> tuple[tuple[str, str], ...]
```

Homepage section buttons that open the icon catalog.

<details>
<summary>Code:</summary>

```python
def icon_section_links(families: list[IconFamily], settings: SiteSettings) -> tuple[tuple[str, str], ...]:
    if not families:
        return ()
    languages = sorted({family.lang for family in families})
    links: list[tuple[str, str]] = []
    for lang in languages:
        label = section_label("icons", lang)
        if len(languages) > 1:
            label = f"{label} ({lang})"
        links.append((label, path_to_url(Path(lang) / "icons")))
    if not links:
        lang = settings.icons_language
        links.append((section_label("icons", lang), path_to_url(Path(lang) / "icons")))
    return tuple(links)
```

</details>

## 🔧 Function `render_icon_grid_html`

```python
def render_icon_grid_html(page: IconGridPage) -> str
```

Render an Icons8-style icon grid (body HTML only).

<details>
<summary>Code:</summary>

```python
def render_icon_grid_html(page: IconGridPage) -> str:
    lang = page.lang
    parts = [
        _GRID_STYLE,
        _breadcrumb(page.crumbs),
        f'<header>\n<h1 class="title">{html.escape(page.heading)}</h1>\n</header>\n',
    ]
    if page.category_links:
        parts.append(_category_row(ui_string(lang, "sections"), page.category_links))
    parts.append(
        '<div class="h-icon-toolbar field">'
        f'<p class="control"><input id="h-icon-search" class="input h-icon-search" type="search" '
        f'placeholder="{html.escape(ui_string(lang, "search_icons"))}" autocomplete="off" /></p>'
        "</div>\n"
    )
    if not page.families:
        parts.append(f"<p>{html.escape(ui_string(lang, 'empty'))}</p>\n")
    else:
        cards = "\n".join(_icon_card(family) for family in page.families)
        parts.append(f'<div id="h-icon-grid" class="h-icon-grid">\n{cards}\n</div>\n')
        parts.append(f'<p id="h-icon-empty" class="h-icon-empty">{html.escape(ui_string(lang, "empty"))}</p>\n')
        parts.append(_pagination(page, lang))
    parts.append(_SEARCH_SCRIPT)
    return "".join(parts)
```

</details>

"""Icons8-style icon grids and per-family pages for the static site."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING

from harrix_pyssg.listing import listing_rel_dir
from harrix_pyssg.site_layout import SiteSettings, path_to_url, section_label, ui_string

if TYPE_CHECKING:
    from harrix_pyssg.icon_catalog import IconFamily

_GRID_STYLE = """
<style>
.h-icon-toolbar { margin: 1rem 0 1.5rem; }
.h-icon-search { max-width: 28rem; }
.h-icon-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(7.5rem, 1fr));
  gap: 0.5rem;
}
.h-icon-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 0.85rem 0.5rem 0.7rem;
  border-radius: 0.6rem;
  color: inherit;
  text-decoration: none;
}
.h-icon-card:hover,
.h-icon-card:focus {
  background: rgba(0, 0, 0, 0.05);
}
[data-theme="dark"] .h-icon-card:hover,
[data-theme="dark"] .h-icon-card:focus {
  background: rgba(255, 255, 255, 0.08);
}
.h-icon-card__img {
  width: 4.5rem;
  height: 4.5rem;
  object-fit: contain;
  display: block;
}
.h-icon-card__label {
  margin-top: 0.55rem;
  font-size: 0.8rem;
  line-height: 1.25;
  color: #6b7280;
  word-break: break-word;
}
.h-icon-card.is-hidden { display: none; }
.h-icon-empty { display: none; margin: 1.5rem 0; }
.h-icon-empty.is-visible { display: block; }
</style>
"""

_SEARCH_SCRIPT = """
<script>
(function () {
  var input = document.getElementById("h-icon-search");
  var grid = document.getElementById("h-icon-grid");
  var empty = document.getElementById("h-icon-empty");
  if (!input || !grid) return;
  var cards = Array.prototype.slice.call(grid.querySelectorAll("[data-search]"));
  input.addEventListener("input", function () {
    var needle = input.value.trim().toLowerCase();
    var shown = 0;
    cards.forEach(function (card) {
      var match = !needle || (card.getAttribute("data-search") || "").indexOf(needle) !== -1;
      card.classList.toggle("is-hidden", !match);
      if (match) shown += 1;
    });
    if (empty) empty.classList.toggle("is-visible", shown === 0);
  });
})();
</script>
"""


@dataclass(frozen=True, slots=True)
class IconGridPage:
    """One generated icon-grid listing page."""

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


def collect_icon_grid_pages(families: list[IconFamily], settings: SiteSettings) -> list[IconGridPage]:
    """Build all-icons and per-category grid pages (with pagination)."""
    if not families:
        return []
    pages: list[IconGridPage] = []
    languages = sorted({family.lang for family in families})
    for lang in languages:
        lang_families = [family for family in families if family.lang == lang]
        pages.extend(_grids_for_language(lang_families, lang, settings))
    return pages


def icon_section_links(families: list[IconFamily], settings: SiteSettings) -> tuple[tuple[str, str], ...]:
    """Homepage section buttons that open the icon catalog."""
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


def render_icon_grid_html(page: IconGridPage) -> str:
    """Render an Icons8-style icon grid (body HTML only)."""
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


def _breadcrumb(crumbs: tuple[tuple[str, str], ...]) -> str:
    """Bulma breadcrumb."""
    if not crumbs:
        return ""
    items: list[str] = []
    last_index = len(crumbs) - 1
    for index, (label, url) in enumerate(crumbs):
        text = html.escape(label)
        if index == last_index:
            items.append(f'<li class="is-active"><a href="{html.escape(url)}" aria-current="page">{text}</a></li>')
        else:
            items.append(f'<li><a href="{html.escape(url)}">{text}</a></li>')
    return '<nav class="breadcrumb" aria-label="breadcrumbs"><ul>\n' + "\n".join(items) + "\n</ul></nav>\n"


def _category_row(title: str, links: tuple[tuple[str, str], ...]) -> str:
    """Category filter chips under the heading."""
    buttons = "".join(
        f'<a class="button is-light is-small" href="{html.escape(url)}">{html.escape(label)}</a>'
        for label, url in links
    )
    return f'<p class="heading">{html.escape(title)}</p>\n<p class="buttons">{buttons}</p>\n'


def _grids_for_language(families: list[IconFamily], lang: str, settings: SiteSettings) -> list[IconGridPage]:
    """All-icons and category grids for one language."""
    pages: list[IconGridPage] = []
    home_crumb = (ui_string(lang, "home"), path_to_url(lang))
    icons_label = section_label("icons", lang)
    icons_base = Path(lang) / "icons"
    categories = sorted({family.category for family in families}, key=str.casefold)
    category_links = [(ui_string(lang, "all_icons"), path_to_url(icons_base))]
    category_links.extend((name, path_to_url(icons_base / name)) for name in categories)
    pages.extend(
        _paged_grids(
            families=families,
            page_base=icons_base,
            lang=lang,
            heading=icons_label,
            title=f"{icons_label} | {settings.site_title}",
            crumbs=(home_crumb, (icons_label, path_to_url(icons_base))),
            category_links=tuple(category_links),
            settings=settings,
        )
    )
    for category in categories:
        cat_families = [family for family in families if family.category == category]
        cat_base = icons_base / category
        pages.extend(
            _paged_grids(
                families=cat_families,
                page_base=cat_base,
                lang=lang,
                heading=category.replace("_", " ").replace("-", " ").capitalize(),
                title=f"{category} | {icons_label} | {settings.site_title}",
                crumbs=(
                    home_crumb,
                    (icons_label, path_to_url(icons_base)),
                    (category, path_to_url(cat_base)),
                ),
                category_links=tuple(category_links),
                settings=settings,
            )
        )
    return pages


def _icon_card(family: IconFamily) -> str:
    """One Icons8-like cell: preview + label."""
    return (
        f'<a class="h-icon-card" href="{html.escape(family.url)}" '
        f'data-search="{html.escape(family.search_text)}">'
        f'<img class="h-icon-card__img" src="{html.escape(family.featured_url)}" '
        f'alt="{html.escape(family.title)}" loading="lazy" />'
        f'<span class="h-icon-card__label">{html.escape(family.title)}</span>'
        "</a>"
    )


def _paged_grids(
    *,
    families: list[IconFamily],
    page_base: Path,
    lang: str,
    heading: str,
    title: str,
    crumbs: tuple[tuple[str, str], ...],
    category_links: tuple[tuple[str, str], ...],
    settings: SiteSettings,
) -> list[IconGridPage]:
    """Split families into `icons_per_page` grid pages."""
    size = max(1, settings.icons_per_page)
    slices = [families[index : index + size] for index in range(0, len(families) or 1, size)]
    if not families:
        slices = [[]]
    page_count = len(slices)
    pages: list[IconGridPage] = []
    for index, slice_families in enumerate(slices, start=1):
        page_title = title if index == 1 else f"{title} — {ui_string(lang, 'page')} {index}"
        pages.append(
            IconGridPage(
                rel_dir=listing_rel_dir(page_base, index),
                title=page_title,
                lang=lang,
                heading=heading,
                families=tuple(slice_families),
                page_num=index,
                page_count=page_count,
                page_base=page_base,
                crumbs=crumbs,
                category_links=category_links,
            )
        )
    return pages


def _pagination(page: IconGridPage, lang: str) -> str:
    """Numbered pagination for a dense icon grid."""
    if page.page_count <= 1:
        return ""
    prev_href = path_to_url(listing_rel_dir(page.page_base, page.page_num - 1)) if page.page_num > 1 else ""
    next_href = (
        path_to_url(listing_rel_dir(page.page_base, page.page_num + 1)) if page.page_num < page.page_count else ""
    )
    prev_attr = f' href="{html.escape(prev_href)}"' if prev_href else " disabled"
    next_attr = f' href="{html.escape(next_href)}"' if next_href else " disabled"
    numbers = []
    for number in range(1, page.page_count + 1):
        href = path_to_url(listing_rel_dir(page.page_base, number))
        current = " is-current" if number == page.page_num else ""
        aria = ' aria-current="page"' if number == page.page_num else ""
        numbers.append(f'<li><a class="pagination-link{current}" href="{html.escape(href)}"{aria}>{number}</a></li>')
    return (
        f'<nav class="pagination is-centered mt-5" role="navigation" '
        f'aria-label="{html.escape(ui_string(lang, "page"))}">'
        f'<a class="pagination-previous"{prev_attr}>{html.escape(ui_string(lang, "newer"))}</a>'
        f'<a class="pagination-next"{next_attr}>{html.escape(ui_string(lang, "older"))}</a>'
        f'<ul class="pagination-list">{"".join(numbers)}</ul></nav>\n'
    )

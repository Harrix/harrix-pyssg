"""HTML for homepage, section, year, taxonomy, and pagination listing pages."""

from __future__ import annotations

import html
from dataclasses import dataclass
from pathlib import Path

from harrix_pyssg.site_layout import (
    CatalogEntry,
    SiteSettings,
    path_to_url,
    section_label,
    slugify_term,
    ui_string,
)


@dataclass(frozen=True, slots=True)
class ListingPage:
    """One generated listing page (a directory with `index.html`)."""

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


def collect_listing_pages(catalog: list[CatalogEntry], settings: SiteSettings) -> list[ListingPage]:
    """Build homepage, language, section, year, category, and tag listing pages."""
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
                section_links=(),
                year_links=(),
                settings=settings,
            )
        )
        return pages

    default_lang = settings.default_language if settings.default_language in languages else languages[0]
    default_home = _language_home_pages(catalog, default_lang, settings)
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
            pages.extend(_language_home_pages(catalog, lang, settings))
        pages.extend(_section_and_taxonomy_pages(catalog, lang, settings))
    return pages


def listing_rel_dir(page_base: Path, page_num: int) -> Path:
    """Return the output directory for listing page number `page_num`."""
    if page_num <= 1:
        return page_base
    return page_base / "page" / str(page_num)


def paginate(items: list[CatalogEntry], per_page: int) -> list[list[CatalogEntry]]:
    """Split catalog entries into pages of `per_page` items (at least one page)."""
    size = max(1, per_page)
    if not items:
        return [[]]
    return [items[index : index + size] for index in range(0, len(items), size)]


def render_listing_html(page: ListingPage) -> str:
    """Render listing body HTML for one page (without theme chrome)."""
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


def _breadcrumb(page: ListingPage) -> str:
    """Bulma breadcrumb from listing crumbs."""
    if not page.crumbs:
        return ""
    items: list[str] = []
    last_index = len(page.crumbs) - 1
    for index, (label, url) in enumerate(page.crumbs):
        text = html.escape(label)
        if index == last_index:
            items.append(f'<li class="is-active"><a href="{html.escape(url)}" aria-current="page">{text}</a></li>')
        else:
            items.append(f'<li><a href="{html.escape(url)}">{text}</a></li>')
    return '<nav class="breadcrumb" aria-label="breadcrumbs"><ul>\n' + "\n".join(items) + "\n</ul></nav>\n"


def _language_home_pages(catalog: list[CatalogEntry], lang: str, settings: SiteSettings) -> list[ListingPage]:
    """Homepage listings for one language (`/{lang}/` and `/{lang}/page/N/`)."""
    entries = [entry for entry in catalog if entry.placement.lang == lang]
    sections = _unique_sections(entries, lang)
    return _paged_listings(
        entries=entries,
        page_base=Path(lang),
        lang=lang,
        heading=settings.site_title,
        title=settings.site_title,
        crumbs=((ui_string(lang, "home"), path_to_url(lang)),),
        section_links=tuple(sections),
        year_links=(),
        settings=settings,
    )


def _link_row(title: str, links: tuple[tuple[str, str], ...]) -> str:
    """Return a row of section, year, or term buttons."""
    buttons = "".join(
        f'<a class="button is-light" href="{html.escape(url)}">{html.escape(label)}</a>' for label, url in links
    )
    return f'<p class="heading">{html.escape(title)}</p>\n<p class="buttons">{buttons}</p>\n'


def _page_window(current: int, total: int) -> list[int]:
    """Page numbers to show: first, last, and a window around the current page."""
    if total <= _PAGINATION_FULL_WINDOW:
        return list(range(1, total + 1))
    chosen = {1, total, current}
    for offset in range(-2, 3):
        value = current + offset
        if 1 <= value <= total:
            chosen.add(value)
    return sorted(chosen)


def _paged_listings(
    *,
    entries: list[CatalogEntry],
    page_base: Path,
    lang: str,
    heading: str,
    title: str,
    crumbs: tuple[tuple[str, str], ...],
    section_links: tuple[tuple[str, str], ...],
    year_links: tuple[tuple[str, str], ...],
    settings: SiteSettings,
) -> list[ListingPage]:
    """Create one `ListingPage` per pagination slice."""
    slices = paginate(entries, settings.per_page)
    page_count = len(slices)
    pages: list[ListingPage] = []
    for index, slice_entries in enumerate(slices, start=1):
        page_title = title if index == 1 else f"{title} — {ui_string(lang, 'page')} {index}"
        pages.append(
            ListingPage(
                rel_dir=listing_rel_dir(page_base, index),
                title=page_title,
                lang=lang,
                heading=heading,
                entries=tuple(slice_entries),
                page_num=index,
                page_count=page_count,
                page_base=page_base,
                crumbs=crumbs,
                section_links=section_links,
                year_links=year_links,
            )
        )
    return pages


def _pagination(page: ListingPage, lang: str) -> str:
    """Bulma pagination when there is more than one page."""
    if page.page_count <= 1:
        return ""
    prev_href = path_to_url(listing_rel_dir(page.page_base, page.page_num - 1)) if page.page_num > 1 else ""
    next_href = (
        path_to_url(listing_rel_dir(page.page_base, page.page_num + 1)) if page.page_num < page.page_count else ""
    )
    prev_attr = f' href="{html.escape(prev_href)}"' if prev_href else " disabled"
    next_attr = f' href="{html.escape(next_href)}"' if next_href else " disabled"
    numbers = []
    shown = _page_window(page.page_num, page.page_count)
    previous = 0
    for number in shown:
        if previous and number > previous + 1:
            numbers.append('<li><span class="pagination-ellipsis">&hellip;</span></li>')
        href = path_to_url(listing_rel_dir(page.page_base, number))
        current = " is-current" if number == page.page_num else ""
        aria = ' aria-current="page"' if number == page.page_num else ""
        numbers.append(f'<li><a class="pagination-link{current}" href="{html.escape(href)}"{aria}>{number}</a></li>')
        previous = number
    return (
        f'<nav class="pagination is-centered" role="navigation" aria-label="{html.escape(ui_string(lang, "page"))}">'
        f'<a class="pagination-previous"{prev_attr}>{html.escape(ui_string(lang, "newer"))}</a>'
        f'<a class="pagination-next"{next_attr}>{html.escape(ui_string(lang, "older"))}</a>'
        f'<ul class="pagination-list">{"".join(numbers)}</ul>'
        "</nav>\n"
    )


def _post_list(entries: tuple[CatalogEntry, ...], lang: str) -> str:
    """Article cards for the current listing page."""
    items: list[str] = []
    for entry in entries:
        date_html = f'<p class="heading">{entry.date.isoformat()}</p>' if entry.date else ""
        image_html = ""
        if entry.featured_image_url:
            image_html = (
                '<figure class="media-left">'
                f'<p class="image is-128x128">'
                f'<a href="{html.escape(entry.url)}">'
                f'<img src="{html.escape(entry.featured_image_url)}" alt="" />'
                f"</a></p></figure>"
            )
        excerpt_html = f"<p>{html.escape(entry.excerpt)}</p>" if entry.excerpt else ""
        meta_bits: list[str] = []
        if entry.placement.section:
            meta_bits.append(
                f'<a href="{html.escape(path_to_url(Path(entry.placement.lang) / entry.placement.section))}">'
                f"{html.escape(section_label(entry.placement.section, lang))}</a>"
            )
        if entry.placement.year:
            meta_bits.append(html.escape(entry.placement.year))
        meta_html = f'<p class="is-size-7">{" · ".join(meta_bits)}</p>' if meta_bits else ""
        items.append(
            '<article class="media h-post-item">'
            f"{image_html}"
            '<div class="media-content">'
            f"{date_html}"
            f'<h2 class="title is-4"><a href="{html.escape(entry.url)}">{html.escape(entry.title)}</a></h2>'
            f"{meta_html}{excerpt_html}"
            "</div></article>"
        )
    return '<div class="h-post-list">\n' + "\n".join(items) + "\n</div>\n"


def _section_and_taxonomy_pages(catalog: list[CatalogEntry], lang: str, settings: SiteSettings) -> list[ListingPage]:
    """Section, year, category, and tag listings for one language."""
    pages: list[ListingPage] = []
    lang_entries = [entry for entry in catalog if entry.placement.lang == lang]
    home_crumb = (ui_string(lang, "home"), path_to_url(lang))

    sections = sorted({entry.placement.section for entry in lang_entries if entry.placement.section})
    for section in sections:
        section_entries = [entry for entry in lang_entries if entry.placement.section == section]
        label = section_label(section, lang)
        section_base = Path(lang) / section
        years = _unique_years(section_entries, lang, section)
        pages.extend(
            _paged_listings(
                entries=section_entries,
                page_base=section_base,
                lang=lang,
                heading=label,
                title=f"{label} | {settings.site_title}",
                crumbs=(home_crumb, (label, path_to_url(section_base))),
                section_links=(),
                year_links=tuple(years),
                settings=settings,
            )
        )
        year_values = sorted({entry.placement.year for entry in section_entries if entry.placement.year}, reverse=True)
        for year in year_values:
            year_entries = [entry for entry in section_entries if entry.placement.year == year]
            year_base = section_base / year
            pages.extend(
                _paged_listings(
                    entries=year_entries,
                    page_base=year_base,
                    lang=lang,
                    heading=f"{label} {year}",
                    title=f"{label} {year} | {settings.site_title}",
                    crumbs=(
                        home_crumb,
                        (label, path_to_url(section_base)),
                        (year, path_to_url(year_base)),
                    ),
                    section_links=(),
                    year_links=(),
                    settings=settings,
                )
            )

    pages.extend(_taxonomy_pages(lang_entries, lang, "categories", "categories", settings, home_crumb))
    pages.extend(_taxonomy_pages(lang_entries, lang, "tags", "tags", settings, home_crumb))
    return pages


def _taxonomy_pages(
    entries: list[CatalogEntry],
    lang: str,
    attr: str,
    folder: str,
    settings: SiteSettings,
    home_crumb: tuple[str, str],
) -> list[ListingPage]:
    """Category or tag index plus one listing per term."""
    terms: dict[str, list[CatalogEntry]] = {}
    for entry in entries:
        for term in getattr(entry, attr):
            terms.setdefault(term, []).append(entry)
    if not terms:
        return []

    pages: list[ListingPage] = []
    index_base = Path(lang) / folder
    index_label = ui_string(lang, folder)
    term_links = tuple((term, path_to_url(index_base / slugify_term(term))) for term in sorted(terms, key=str.casefold))
    pages.append(
        ListingPage(
            rel_dir=index_base,
            title=f"{index_label} | {settings.site_title}",
            lang=lang,
            heading=index_label,
            entries=(),
            page_num=1,
            page_count=1,
            page_base=index_base,
            crumbs=(home_crumb, (index_label, path_to_url(index_base))),
            section_links=term_links,
            year_links=(),
        )
    )
    for term, term_entries in sorted(terms.items(), key=lambda item: item[0].casefold()):
        term_base = index_base / slugify_term(term)
        pages.extend(
            _paged_listings(
                entries=term_entries,
                page_base=term_base,
                lang=lang,
                heading=term,
                title=f"{term} | {settings.site_title}",
                crumbs=(
                    home_crumb,
                    (index_label, path_to_url(index_base)),
                    (term, path_to_url(term_base)),
                ),
                section_links=(),
                year_links=(),
                settings=settings,
            )
        )
    return pages


def _unique_sections(entries: list[CatalogEntry], lang: str) -> list[tuple[str, str]]:
    """Section buttons for a language homepage."""
    names = sorted({entry.placement.section for entry in entries if entry.placement.section})
    return [(section_label(name, lang), path_to_url(Path(lang) / name)) for name in names]


def _unique_years(entries: list[CatalogEntry], lang: str, section: str) -> list[tuple[str, str]]:
    """Year buttons for a section listing."""
    years = sorted({entry.placement.year for entry in entries if entry.placement.year}, reverse=True)
    return [(year, path_to_url(Path(lang) / section / year)) for year in years]


_PAGINATION_FULL_WINDOW = 7

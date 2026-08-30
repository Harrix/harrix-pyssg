"""Harrix PySSG — Simple static site generator in Python."""

from .article import Article
from .icon_catalog import IconFamily, load_icon_families
from .icon_pages import IconGridPage, collect_icon_grid_pages, render_icon_grid_html
from .listing import ListingPage, collect_listing_pages, paginate, render_listing_html
from .note_meta import (
    ResolvedNoteDate,
    resolve_note_date,
    resolve_note_date_for_path,
    resolve_note_title,
    title_from_id,
)
from .page_assembler import PageAssembler, PageFeatures, detect_page_features, extract_title
from .site_layout import CatalogEntry, SiteSettings, build_catalog, place_article
from .static_site_generator import StaticSiteGenerator
from .theme_slicer import ThemeSlicer

__all__ = [
    "Article",
    "CatalogEntry",
    "IconFamily",
    "IconGridPage",
    "ListingPage",
    "PageAssembler",
    "PageFeatures",
    "ResolvedNoteDate",
    "SiteSettings",
    "StaticSiteGenerator",
    "ThemeSlicer",
    "build_catalog",
    "collect_icon_grid_pages",
    "collect_listing_pages",
    "detect_page_features",
    "extract_title",
    "load_icon_families",
    "paginate",
    "place_article",
    "render_icon_grid_html",
    "render_listing_html",
    "resolve_note_date",
    "resolve_note_date_for_path",
    "resolve_note_title",
    "title_from_id",
]

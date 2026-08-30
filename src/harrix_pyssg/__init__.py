"""Harrix PySSG — Simple static site generator in Python."""

from .article import Article
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
    "ListingPage",
    "PageAssembler",
    "PageFeatures",
    "ResolvedNoteDate",
    "SiteSettings",
    "StaticSiteGenerator",
    "ThemeSlicer",
    "build_catalog",
    "collect_listing_pages",
    "detect_page_features",
    "extract_title",
    "paginate",
    "place_article",
    "render_listing_html",
    "resolve_note_date",
    "resolve_note_date_for_path",
    "resolve_note_title",
    "title_from_id",
]

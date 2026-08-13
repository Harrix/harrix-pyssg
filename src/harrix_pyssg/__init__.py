"""Harrix PySSG — Simple static site generator in Python."""

from .article import Article
from .note_meta import (
    ResolvedNoteDate,
    resolve_note_date,
    resolve_note_date_for_path,
    resolve_note_title,
    title_from_id,
)
from .page_assembler import PageAssembler, PageFeatures, detect_page_features, extract_title
from .static_site_generator import StaticSiteGenerator
from .theme_slicer import ThemeSlicer

__all__ = [
    "Article",
    "PageAssembler",
    "PageFeatures",
    "ResolvedNoteDate",
    "StaticSiteGenerator",
    "ThemeSlicer",
    "detect_page_features",
    "extract_title",
    "resolve_note_date",
    "resolve_note_date_for_path",
    "resolve_note_title",
    "title_from_id",
]

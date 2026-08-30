"""Map content folders to harrix.dev-style site paths and listing catalogs."""

from __future__ import annotations

import datetime
import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import TYPE_CHECKING, Any
from urllib.parse import quote

from harrix_pyssg.note_meta import resolve_note_date, resolve_note_title

if TYPE_CHECKING:
    from harrix_pyssg.article import Article

_LANG_RE = re.compile(r"^(en|ru)$", re.IGNORECASE)
_YEAR_RE = re.compile(r"^\d{4}$")
_SAFE_SLUG_RE = re.compile(r"^[A-Za-z0-9._-]+$")
_MD_LINK_RE = re.compile(r"\[([^\]]*)\]\([^)]+\)")
_MD_IMAGE_RE = re.compile(r"!\[([^\]]*)\]\([^)]+\)")
_MD_EMPHASIS_RE = re.compile(r"[*_`]+")
_MD_SKIP_PREFIXES = ("#", "```", ">", "- ", "![")
_MIN_REPO_TAIL_PARTS = 2
_ARTICLE_FOLDER_MIN_PARTS = 2
_SITE_TREE_MIN_PARTS = 3
_SITE_TREE_WITH_YEAR_PARTS = 4
_EXCERPT_LIMIT = 280

_UI_DATA = json.loads(Path(__file__).with_name("listing_ui.json").read_text(encoding="utf8"))
SECTION_LABELS: dict[str, dict[str, str]] = _UI_DATA["sections"]
UI_STRINGS: dict[str, dict[str, str]] = _UI_DATA["ui"]


@dataclass(frozen=True, slots=True)
class ArticlePlacement:
    """Where one article lives on the generated site."""

    lang: str
    slug: str
    rel_output: Path
    section: str | None = None
    year: str | None = None


@dataclass(slots=True)
class CatalogEntry:
    """Published article ready for listing pages."""

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


@dataclass(frozen=True, slots=True)
class SiteSettings:
    """Site-wide defaults used when placing articles and building listings."""

    site_name: str = "harrix.dev"
    default_language: str = "ru"
    site_title: str = "Harrix"
    per_page: int = 20
    icons_per_page: int = 96
    icons_language: str = "en"


def as_string_list(value: Any) -> list[str]:
    """Normalize a YAML list or scalar into a list of non-empty strings."""
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


def build_catalog(articles: list[Article], md_folder: Path, settings: SiteSettings) -> list[CatalogEntry]:
    """Build a newest-first catalog of published articles."""
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


def excerpt_from_markdown(md_content: str, limit: int = _EXCERPT_LIMIT) -> str:
    """Take the first prose paragraph from Markdown as a short excerpt."""
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


def is_published(yaml_dict: dict[str, Any] | None) -> bool:
    """Return `False` only when YAML explicitly sets `published: false`."""
    if not yaml_dict:
        return True
    return yaml_dict.get("published", True) is not False


def parse_content_repo_name(repo_name: str, settings: SiteSettings) -> ArticlePlacement | None:
    """Parse `{site}-{section}[-{year}][-{lang}]` into placement without a slug."""
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


def path_to_url(rel_dir: Path | str) -> str:
    """Turn a relative output directory into a site-absolute folder URL."""
    text = rel_dir.as_posix() if isinstance(rel_dir, Path) else str(rel_dir).replace("\\", "/")
    text = text.strip("/")
    return f"/{text}/" if text else "/"


def place_article(article: Article, md_folder: Path, settings: SiteSettings) -> ArticlePlacement:
    """Resolve the output directory and URL parts for one article.

    Supports:

    - content-repo root: `{site}-{section}[-year][-lang]/{slug}/{slug}.md`
    - site-repo tree: `{lang}/{section}/[{year}/]{slug}/{slug}.md`
    - flat folders: keep the relative parent path of the Markdown file

    """
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


def section_label(section: str, lang: str) -> str:
    """Localized label for a content section (`articles`, `games`, …)."""
    labels = SECTION_LABELS.get(section)
    if labels:
        return labels.get(lang) or labels.get("en") or section
    return section.replace("-", " ").capitalize()


def slugify_term(value: str) -> str:
    """Make a URL segment from a category or tag."""
    text = value.strip()
    if _SAFE_SLUG_RE.fullmatch(text):
        return text
    return quote(text.replace(" ", "-"), safe="-_.")


def ui_string(lang: str, key: str) -> str:
    """Return a listing UI string for `lang`, falling back to English."""
    table = UI_STRINGS.get(lang) or UI_STRINGS["en"]
    return table.get(key) or UI_STRINGS["en"].get(key, key)


def _article_date(article: Article) -> datetime.date | None:
    """Resolve the article date from YAML or the filename."""
    resolved = resolve_note_date(article.md_content, file_name=article.md_filename.name)
    if resolved is None:
        return None
    return resolved.value


def _article_rel_output(lang: str, section: str, year: str | None, slug: str) -> Path:
    """Build `{lang}/{section}/[{year}/]{slug}`."""
    parts = [lang, section]
    if year:
        parts.append(year)
    parts.append(slug)
    return Path(*parts)


def _catalog_sort_key(entry: CatalogEntry) -> tuple[int, str]:
    """Sort listings by date descending, then title."""
    day = entry.date or datetime.date.min
    return (-day.toordinal(), entry.title.casefold())

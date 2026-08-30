"""Load Harrix-Vector-Icons note-folder catalogs for the static site."""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import yaml

from harrix_pyssg.site_layout import as_string_list

_DEFAULT_FEATURED = "featured-image.svg"
_ICONS_FOLDER_MIN_PARTS = 2


@dataclass(slots=True)
class IconFamily:
    """One icon family (note folder with a featured image and variants)."""

    icon_id: str
    title: str
    folder: str
    featured: str
    lang: str
    categories: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    note_name: str = ""

    @property
    def category(self) -> str:
        """Primary category used in the site URL."""
        if self.categories:
            return self.categories[0]
        parts = [part for part in self.folder.replace("\\", "/").split("/") if part]
        if len(parts) >= _ICONS_FOLDER_MIN_PARTS and parts[0] == "icons":
            return parts[1]
        return parts[0] if parts else "icons"

    def featured_path(self, repo_root: Path) -> Path | None:
        """Return the featured image file when it exists."""
        name = self.featured or _DEFAULT_FEATURED
        path = repo_root.joinpath(*self.folder.replace("\\", "/").split("/"), name)
        return path if path.is_file() else None

    @property
    def featured_url(self) -> str:
        """Site-absolute URL of the featured SVG."""
        name = self.featured or _DEFAULT_FEATURED
        return f"{self.url}{name}"

    def note_path(self, repo_root: Path) -> Path | None:
        """Return the family Markdown file when it exists."""
        name = self.note_name or f"{self.icon_id}.md"
        path = repo_root.joinpath(*self.folder.replace("\\", "/").split("/"), name)
        return path if path.is_file() else None

    @property
    def rel_output(self) -> Path:
        """Site-relative folder `{lang}/icons/{category}/{id}`."""
        return Path(self.lang) / "icons" / self.category / self.icon_id

    @property
    def search_text(self) -> str:
        """Lowercased blob used by the client-side icon search."""
        parts = [self.icon_id, self.title, self.category, *self.categories, *self.tags]
        return " ".join(parts).casefold()

    @property
    def url(self) -> str:
        """Site-absolute URL of the icon family page."""
        return f"/{self.rel_output.as_posix()}/"


def load_icon_families(icons_path: str | Path, *, default_lang: str = "en") -> list[IconFamily]:
    """Load icon families from a repo root or an `icons/` folder.

    Prefers `catalog.json` when present; otherwise scans note folders.

    Args:

    - `icons_path` (`str | Path`): Vector-icons repo root or its `icons/` folder.
    - `default_lang` (`str`): Language segment when a note has no `lang` key.

    Returns:

    - `list[IconFamily]`: Families sorted by title.

    """
    repo_root = resolve_icons_repo_root(icons_path)
    catalog_file = repo_root / "catalog.json"
    if catalog_file.is_file():
        families = _families_from_catalog(catalog_file, repo_root, default_lang=default_lang)
    else:
        families = _scan_icon_notes(repo_root, default_lang=default_lang)
    families.sort(key=lambda item: (item.title.casefold(), item.icon_id))
    return families


def resolve_icons_repo_root(icons_path: str | Path) -> Path:
    """Normalize a repo root or `icons/` folder to the repository root."""
    path = Path(icons_path).expanduser().resolve()
    if path.name == "icons" and path.is_dir():
        return path.parent
    return path


def _families_from_catalog(catalog_file: Path, repo_root: Path, *, default_lang: str) -> list[IconFamily]:
    """Build families from `catalog.json`."""
    raw = json.loads(catalog_file.read_text(encoding="utf8"))
    families: list[IconFamily] = []
    for item in raw.get("icons") or []:
        if not isinstance(item, dict):
            continue
        family = _family_from_catalog_item(item, repo_root, default_lang=default_lang)
        if family is not None:
            families.append(family)
    return families


def _family_from_catalog_item(item: dict[str, Any], repo_root: Path, *, default_lang: str) -> IconFamily | None:
    """Convert one `catalog.json` object into an `IconFamily`."""
    icon_id = str(item.get("id") or "").strip()
    folder = str(item.get("folder") or "").strip().replace("\\", "/")
    if not icon_id or not folder:
        return None
    title = str(item.get("title") or icon_id).strip()
    featured = str(item.get("featured") or _DEFAULT_FEATURED).strip()
    note_path = repo_root.joinpath(*folder.split("/"), f"{icon_id}.md")
    lang = default_lang
    if note_path.is_file():
        lang = _lang_from_note(note_path, default_lang)
    return IconFamily(
        icon_id=icon_id,
        title=title,
        folder=folder,
        featured=featured,
        lang=lang,
        categories=as_string_list(item.get("categories")),
        tags=as_string_list(item.get("tags")),
        note_name=f"{icon_id}.md",
    )


def _lang_from_note(note_path: Path, default_lang: str) -> str:
    """Read `lang` from a note file."""
    return _lang_from_yaml(_yaml_dict_from_note(note_path), default_lang)


def _lang_from_yaml(yaml_dict: dict[str, Any], default_lang: str) -> str:
    """Return a two-letter language or `default_lang`."""
    lang = str(yaml_dict.get("lang") or "").strip().lower()
    return lang if lang in {"en", "ru"} else default_lang


def _scan_icon_notes(repo_root: Path, *, default_lang: str) -> list[IconFamily]:
    """Scan `icons/**/{id}/{id}.md` note folders when `catalog.json` is missing."""
    icons_dir = repo_root / "icons"
    root = icons_dir if icons_dir.is_dir() else repo_root
    families: list[IconFamily] = []
    for note in root.rglob("*.md"):
        if note.name.startswith(".") or any(part.startswith(".") for part in note.parts):
            continue
        if note.stem != note.parent.name:
            continue
        rel_folder = note.parent.relative_to(repo_root).as_posix()
        featured = _DEFAULT_FEATURED if (note.parent / _DEFAULT_FEATURED).is_file() else ""
        yaml_dict = _yaml_dict_from_note(note)
        families.append(
            IconFamily(
                icon_id=note.stem,
                title=_title_from_note(note, yaml_dict),
                folder=rel_folder,
                featured=featured,
                lang=_lang_from_yaml(yaml_dict, default_lang),
                categories=as_string_list(yaml_dict.get("categories")),
                tags=as_string_list(yaml_dict.get("tags")),
                note_name=note.name,
            )
        )
    return families


def _title_from_note(note_path: Path, yaml_dict: dict[str, Any]) -> str:
    """Prefer YAML `title`, then the first H1, then the folder ID."""
    title = str(yaml_dict.get("title") or "").strip()
    if title:
        return title
    try:
        text = note_path.read_text(encoding="utf8")
    except OSError:
        return note_path.stem
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("# "):
            return stripped[2:].strip() or note_path.stem
    return note_path.stem


def _yaml_dict_from_note(note_path: Path) -> dict[str, Any]:
    """Parse note front matter without requiring a full Article load."""
    try:
        text = note_path.read_text(encoding="utf8").lstrip("\ufeff")
    except OSError:
        return {}
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end < 0:
        return {}
    raw = text[3:end].strip()
    if not raw:
        return {}
    loaded = yaml.safe_load(raw)
    return loaded if isinstance(loaded, dict) else {}

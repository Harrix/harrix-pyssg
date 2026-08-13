"""Re-export note title/date resolvers from harrix-pylib.

@hsk-sync:note-meta — Python source of truth is `harrix_pylib.note_meta`.
Keep JS and Android implementations aligned with that module.

"""

from harrix_pylib.note_meta import (
    ResolvedNoteDate,
    extract_title_from_markdown,
    note_stem_from_name,
    parse_date_from_file_name,
    parse_date_from_yaml,
    parse_date_value,
    resolve_note_date,
    resolve_note_date_for_path,
    resolve_note_title,
    title_from_id,
)

__all__ = [
    "ResolvedNoteDate",
    "extract_title_from_markdown",
    "note_stem_from_name",
    "parse_date_from_file_name",
    "parse_date_from_yaml",
    "parse_date_value",
    "resolve_note_date",
    "resolve_note_date_for_path",
    "resolve_note_title",
    "title_from_id",
]

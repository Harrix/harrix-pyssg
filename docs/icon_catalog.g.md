---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# 📄 File `icon_catalog.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🏛️ Class `IconFamily`](#%EF%B8%8F-class-iconfamily)
  - [⚙️ Method `category (property)`](#%EF%B8%8F-method-category-property)
  - [⚙️ Method `featured_path`](#%EF%B8%8F-method-featured_path)
  - [⚙️ Method `featured_url (property)`](#%EF%B8%8F-method-featured_url-property)
  - [⚙️ Method `note_path`](#%EF%B8%8F-method-note_path)
  - [⚙️ Method `rel_output (property)`](#%EF%B8%8F-method-rel_output-property)
  - [⚙️ Method `search_text (property)`](#%EF%B8%8F-method-search_text-property)
  - [⚙️ Method `url (property)`](#%EF%B8%8F-method-url-property)
- [🔧 Function `load_icon_families`](#-function-load_icon_families)
- [🔧 Function `resolve_icons_repo_root`](#-function-resolve_icons_repo_root)

</details>

## 🏛️ Class `IconFamily`

```python
class IconFamily
```

One icon family (note folder with a featured image and variants).

<details>
<summary>Code:</summary>

```python
class IconFamily:

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
```

</details>

### ⚙️ Method `category (property)`

```python
def category(self) -> str
```

Primary category used in the site URL.

<details>
<summary>Code:</summary>

```python
def category(self) -> str:
        if self.categories:
            return self.categories[0]
        parts = [part for part in self.folder.replace("\\", "/").split("/") if part]
        if len(parts) >= _ICONS_FOLDER_MIN_PARTS and parts[0] == "icons":
            return parts[1]
        return parts[0] if parts else "icons"
```

</details>

### ⚙️ Method `featured_path`

```python
def featured_path(self, repo_root: Path) -> Path | None
```

Return the featured image file when it exists.

<details>
<summary>Code:</summary>

```python
def featured_path(self, repo_root: Path) -> Path | None:
        name = self.featured or _DEFAULT_FEATURED
        path = repo_root.joinpath(*self.folder.replace("\\", "/").split("/"), name)
        return path if path.is_file() else None
```

</details>

### ⚙️ Method `featured_url (property)`

```python
def featured_url(self) -> str
```

Site-absolute URL of the featured SVG.

<details>
<summary>Code:</summary>

```python
def featured_url(self) -> str:
        name = self.featured or _DEFAULT_FEATURED
        return f"{self.url}{name}"
```

</details>

### ⚙️ Method `note_path`

```python
def note_path(self, repo_root: Path) -> Path | None
```

Return the family Markdown file when it exists.

<details>
<summary>Code:</summary>

```python
def note_path(self, repo_root: Path) -> Path | None:
        name = self.note_name or f"{self.icon_id}.md"
        path = repo_root.joinpath(*self.folder.replace("\\", "/").split("/"), name)
        return path if path.is_file() else None
```

</details>

### ⚙️ Method `rel_output (property)`

```python
def rel_output(self) -> Path
```

Site-relative folder `{lang}/icons/{category}/{id}`.

<details>
<summary>Code:</summary>

```python
def rel_output(self) -> Path:
        return Path(self.lang) / "icons" / self.category / self.icon_id
```

</details>

### ⚙️ Method `search_text (property)`

```python
def search_text(self) -> str
```

Lowercased blob used by the client-side icon search.

<details>
<summary>Code:</summary>

```python
def search_text(self) -> str:
        parts = [self.icon_id, self.title, self.category, *self.categories, *self.tags]
        return " ".join(parts).casefold()
```

</details>

### ⚙️ Method `url (property)`

```python
def url(self) -> str
```

Site-absolute URL of the icon family page.

<details>
<summary>Code:</summary>

```python
def url(self) -> str:
        return f"/{self.rel_output.as_posix()}/"
```

</details>

## 🔧 Function `load_icon_families`

```python
def load_icon_families(icons_path: str | Path, *, default_lang: str = 'en') -> list[IconFamily]
```

Load icon families from a repo root or an `icons/` folder.

Prefers `catalog.json` when present; otherwise scans note folders.

Args:

- `icons_path` (`str | Path`): Vector-icons repo root or its `icons/` folder.
- `default_lang` (`str`): Language segment when a note has no `lang` key.

Returns:

- `list[IconFamily]`: Families sorted by title.

<details>
<summary>Code:</summary>

```python
def load_icon_families(icons_path: str | Path, *, default_lang: str = "en") -> list[IconFamily]:
    repo_root = resolve_icons_repo_root(icons_path)
    catalog_file = repo_root / "catalog.json"
    if catalog_file.is_file():
        families = _families_from_catalog(catalog_file, repo_root, default_lang=default_lang)
    else:
        families = _scan_icon_notes(repo_root, default_lang=default_lang)
    families.sort(key=lambda item: (item.title.casefold(), item.icon_id))
    return families
```

</details>

## 🔧 Function `resolve_icons_repo_root`

```python
def resolve_icons_repo_root(icons_path: str | Path) -> Path
```

Normalize a repo root or `icons/` folder to the repository root.

<details>
<summary>Code:</summary>

```python
def resolve_icons_repo_root(icons_path: str | Path) -> Path:
    path = Path(icons_path).expanduser().resolve()
    if path.name == "icons" and path.is_dir():
        return path.parent
    return path
```

</details>

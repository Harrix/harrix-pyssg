"""Assemble full HTML pages from sliced theme parts and article content."""

from __future__ import annotations

import json
import re
import shutil
from dataclasses import dataclass
from pathlib import Path

from harrix_pyssg.theme_slicer import (
    ASSET_DIRS,
    PLACEHOLDER_CONTENT,
    PLACEHOLDER_OPTIONAL_HEAD,
    PLACEHOLDER_OPTIONAL_SCRIPTS,
    PLACEHOLDER_TITLE,
)

_H1_RE = re.compile(r"<h1\b[^>]*>(.*?)</h1>", re.IGNORECASE | re.DOTALL)
_TAG_RE = re.compile(r"<[^>]+>")
_ASSET_ATTR_RE = re.compile(
    r"""\b(href|src)=(["'])(\.?/)?(""" + "|".join(ASSET_DIRS) + r""")/""",
    re.IGNORECASE,
)
_MERMAID_FENCE_RE = re.compile(r"^```\s*mermaid\b", re.IGNORECASE | re.MULTILINE)
_CHART_FENCE_RE = re.compile(r"^```\s*chart\b", re.IGNORECASE | re.MULTILINE)
_STL_RE = re.compile(r"""class=["'][^"']*\bh-stl-viewer\b|```\s*stl\b""", re.IGNORECASE)
_MATH_DOLLAR_RE = re.compile(r"(?<!\\)\$(?!\$).+?(?<!\\)\$", re.DOTALL)
_MATH_HTML_RE = re.compile(r"""class=["'][^"']*\b(?:tex|math|katex)\b""", re.IGNORECASE)


class PageAssembler:
    """Build a full HTML page from theme parts and article body HTML.

    ## Usage examples

    ```python
    import harrix_pyssg as hsg

    assembler = hsg.PageAssembler("./theme")
    html = assembler.assemble(
        content_html="<h1>Title</h1><p>Hello</p>",
        title="Title",
        features=hsg.PageFeatures(katex=True),
        asset_prefix="../",
    )
    ```

    """

    def __init__(self, theme_dir: str | Path) -> None:
        """Load sliced theme parts from `theme_dir`.

        Args:

        - `theme_dir` (`str | Path`): Folder created by `ThemeSlicer.slice()`.

        """
        self.theme_dir = Path(theme_dir)
        parts_dir = self.theme_dir / "parts"
        if not parts_dir.is_dir():
            msg = f"Theme parts not found: {parts_dir}"
            raise FileNotFoundError(msg)

        self.parts = {
            "head": (parts_dir / "head.html").read_text(encoding="utf8"),
            "body_open": (parts_dir / "body_open.html").read_text(encoding="utf8"),
            "chrome_header": (parts_dir / "chrome_header.html").read_text(encoding="utf8"),
            "main": (parts_dir / "main.html").read_text(encoding="utf8"),
            "chrome_footer": (parts_dir / "chrome_footer.html").read_text(encoding="utf8"),
            "scripts": (parts_dir / "scripts.html").read_text(encoding="utf8"),
            "document_end": (parts_dir / "document_end.html").read_text(encoding="utf8"),
        }
        optional_dir = parts_dir / "optional"
        self.optional = {
            path.stem: path.read_text(encoding="utf8").strip() for path in optional_dir.glob("*.html") if path.is_file()
        }
        manifest_path = self.theme_dir / "manifest.json"
        self.manifest = json.loads(manifest_path.read_text(encoding="utf8")) if manifest_path.is_file() else {}

    def assemble(
        self,
        content_html: str,
        title: str,
        features: PageFeatures | None = None,
        asset_prefix: str = "",
    ) -> str:
        """Assemble a full HTML document.

        Args:

        - `content_html` (`str`): Article body HTML (without chrome).
        - `title` (`str`): Document title for `<title>`.
        - `features` (`PageFeatures | None`): Optional assets to include.
        - `asset_prefix` (`str`): Relative prefix to theme assets from the page
          (for example `../../`). Empty means assets live next to the page.

        Returns:

        - `str`: Full HTML page.

        """
        features = features or PageFeatures()
        optional_head_bits: list[str] = []
        optional_script_bits: list[str] = []

        if features.katex:
            if self.optional.get("katex_css"):
                optional_head_bits.append(self.optional["katex_css"])
            if self.optional.get("katex_js"):
                optional_script_bits.append(self.optional["katex_js"])
        if features.stl:
            if self.optional.get("stl_css"):
                optional_head_bits.append(self.optional["stl_css"])
            if self.optional.get("stl_js"):
                optional_script_bits.append(self.optional["stl_js"])

        optional_head = ("\n    ".join(optional_head_bits) + "\n") if optional_head_bits else ""
        optional_scripts = ("\n    ".join(optional_script_bits) + "\n") if optional_script_bits else ""

        chunks = [
            self.parts["head"],
            self.parts["body_open"],
            self.parts["chrome_header"],
            self.parts["main"],
            self.parts["chrome_footer"],
            self.parts["scripts"],
            self.parts["document_end"],
        ]
        page = "".join(chunks)
        page = page.replace(PLACEHOLDER_TITLE, _escape_html(title))
        page = page.replace(PLACEHOLDER_CONTENT, content_html)
        page = page.replace(PLACEHOLDER_OPTIONAL_HEAD, optional_head)
        page = page.replace(PLACEHOLDER_OPTIONAL_SCRIPTS, optional_scripts)
        return rewrite_asset_paths(page, asset_prefix)

    def copy_assets_to(self, site_root: str | Path) -> None:
        """Copy theme asset directories into the site output root.

        Args:

        - `site_root` (`str | Path`): Site output folder (HTML root).

        """
        site_root = Path(site_root)
        site_root.mkdir(parents=True, exist_ok=True)
        asset_dirs = self.manifest.get("asset_dirs", [name for name in ASSET_DIRS if (self.theme_dir / name).is_dir()])
        for name in asset_dirs:
            src = self.theme_dir / name
            if not src.is_dir():
                continue
            dest = site_root / name
            if dest.exists():
                shutil.rmtree(dest)
            shutil.copytree(src, dest)


@dataclass(frozen=True)
class PageFeatures:
    """Optional page features detected from Markdown/HTML/YAML."""

    katex: bool = False
    stl: bool = False
    mermaid: bool = False
    chart: bool = False


def asset_prefix_for(page_dir: str | Path, site_root: str | Path) -> str:
    """Build a relative prefix from a page directory to the site root.

    Args:

    - `page_dir` (`str | Path`): Directory of the page `index.html`.
    - `site_root` (`str | Path`): Site output root that holds `css/`, `js/`, …

    Returns:

    - `str`: Prefix such as `""`, `../`, or `../../`.

    """
    page_dir = Path(page_dir).resolve()
    site_root = Path(site_root).resolve()
    try:
        relative = page_dir.relative_to(site_root)
    except ValueError:
        return ""
    depth = len(relative.parts)
    if depth == 0:
        return ""
    return "../" * depth


def detect_page_features(
    content_html: str,
    md_content: str = "",
    yaml_dict: dict | None = None,
) -> PageFeatures:
    """Detect optional features from rendered HTML, Markdown, and YAML.

    Args:

    - `content_html` (`str`): Rendered article HTML.
    - `md_content` (`str`): Raw Markdown (may include fences).
    - `yaml_dict` (`dict | None`): Front matter dictionary.

    Returns:

    - `PageFeatures`: Detected optional features.

    """
    yaml_dict = yaml_dict or {}
    latex_flag = bool(yaml_dict.get("latex", False))
    katex = (
        latex_flag
        or bool(_MATH_DOLLAR_RE.search(md_content))
        or bool(_MATH_HTML_RE.search(content_html))
        or "katex" in content_html.lower()
    )
    stl = bool(_STL_RE.search(md_content) or _STL_RE.search(content_html))
    mermaid = bool(
        _MERMAID_FENCE_RE.search(md_content) or 'class="mermaid"' in content_html or "class='mermaid'" in content_html
    )
    chart = bool(
        _CHART_FENCE_RE.search(md_content) or "language-chart" in content_html or 'class="chart"' in content_html
    )
    return PageFeatures(katex=katex, stl=stl, mermaid=mermaid, chart=chart)


def extract_title(content_html: str, fallback: str = "Untitled") -> str:
    """Extract plain-text title from the first `<h1>` in HTML.

    Args:

    - `content_html` (`str`): Article HTML.
    - `fallback` (`str`): Title used when no `<h1>` is present.

    Returns:

    - `str`: Plain title text.

    """
    match = _H1_RE.search(content_html)
    if match is None:
        return fallback
    return _TAG_RE.sub("", match.group(1)).strip() or fallback


def rewrite_asset_paths(html: str, asset_prefix: str) -> str:
    """Prefix theme asset `href`/`src` values with `asset_prefix`.

    Args:

    - `html` (`str`): Full or partial HTML.
    - `asset_prefix` (`str`): Relative prefix (`../`, `../../`, …).

    Returns:

    - `str`: HTML with rewritten asset paths.

    """
    if not asset_prefix:
        # Normalize "./css/..." to "css/..."
        return _ASSET_ATTR_RE.sub(r"\1=\2\4/", html)

    def _replace(match: re.Match[str]) -> str:
        attr, quote, _dot, folder = match.groups()
        return f"{attr}={quote}{asset_prefix}{folder}/"

    return _ASSET_ATTR_RE.sub(_replace, html)


def _escape_html(text: str) -> str:
    """Escape text for HTML text nodes and attribute-safe titles."""
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;")

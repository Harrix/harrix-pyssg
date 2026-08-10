"""Slice a built Harrix HTML template into theme parts for the SSG."""

from __future__ import annotations

import json
import re
import shutil
from pathlib import Path

PLACEHOLDER_TITLE = "{{H_SSG_TITLE}}"
PLACEHOLDER_CONTENT = "{{H_SSG_CONTENT}}"
PLACEHOLDER_OPTIONAL_HEAD = "{{H_SSG_OPTIONAL_HEAD}}"
PLACEHOLDER_OPTIONAL_SCRIPTS = "{{H_SSG_OPTIONAL_SCRIPTS}}"

MARKER_OPTIONAL_HEAD = "<!-- h-ssg:optional-head -->"
MARKER_OPTIONAL_SCRIPTS = "<!-- h-ssg:optional-scripts -->"
MARKER_CHROME_HEADER_START = "<!-- h-ssg:chrome-header-start -->"
MARKER_CHROME_HEADER_END = "<!-- h-ssg:chrome-header-end -->"
MARKER_CONTENT_START = "<!-- h-ssg:content-start -->"
MARKER_CONTENT_END = "<!-- h-ssg:content-end -->"
MARKER_CHROME_FOOTER_START = "<!-- h-ssg:chrome-footer-start -->"
MARKER_CHROME_FOOTER_END = "<!-- h-ssg:chrome-footer-end -->"

OPTIONAL_ASSET_PATTERNS: dict[str, re.Pattern[str]] = {
    "katex_css": re.compile(r"""<link\b[^>]*href=["'][^"']*katex/katex\.css["'][^>]*/?>""", re.IGNORECASE),
    "katex_js": re.compile(r"""<script\b[^>]*src=["'][^"']*katex/katex\.js["'][^>]*>\s*</script>""", re.IGNORECASE),
    "stl_css": re.compile(r"""<link\b[^>]*href=["'][^"']*stl-viewer/stl-viewer\.css["'][^>]*/?>""", re.IGNORECASE),
    "stl_js": re.compile(
        r"""<script\b[^>]*src=["'][^"']*stl-viewer/stl-viewer\.js["'][^>]*>\s*</script>""",
        re.IGNORECASE,
    ),
}

ASSET_DIRS = ("css", "js", "fonts", "favicon", "img", "images", "katex", "charts")

_TITLE_RE = re.compile(r"(<title>)(.*?)(</title>)", re.IGNORECASE | re.DOTALL)
_BODY_OPEN_RE = re.compile(r"<body\b[^>]*>", re.IGNORECASE)
_MAIN_RE = re.compile(r"<main\b[^>]*>.*?</main>", re.IGNORECASE | re.DOTALL)


class ThemeSlicer:
    """Cut a built HTML template page into reusable theme parts and assets.

    ## Usage examples

    ```python
    import harrix_pyssg as hsg

    slicer = hsg.ThemeSlicer(
        dist_dir="D:/GitHub/Harrix-HTML-Template/dist",
        theme_dir="./theme",
        source_html="article.html",
    )
    slicer.slice()
    ```

    ## Output layout

    ```text
    theme/
    ├─ manifest.json
    ├─ parts/
    │  ├─ head.html
    │  ├─ body_open.html
    │  ├─ chrome_header.html
    │  ├─ main.html
    │  ├─ chrome_footer.html
    │  ├─ scripts.html
    │  ├─ document_end.html
    │  └─ optional/
    │     ├─ katex_css.html
    │     ├─ katex_js.html
    │     ├─ stl_css.html
    │     └─ stl_js.html
    ├─ css/
    ├─ js/
    └─ …
    ```

    """

    def __init__(
        self,
        dist_dir: str | Path,
        theme_dir: str | Path,
        source_html: str = "article.html",
    ) -> None:
        """Prepare paths for slicing a built template.

        Args:

        - `dist_dir` (`str | Path`): Folder with built template HTML and assets
          (for example `Harrix-HTML-Template/dist`).
        - `theme_dir` (`str | Path`): Output folder for sliced theme parts and assets.
        - `source_html` (`str`): HTML page used as the article shell. Defaults to
          `article.html`.

        """
        self.dist_dir = Path(dist_dir)
        self.theme_dir = Path(theme_dir)
        self.source_html = source_html

    def slice(self) -> Path:
        """Slice the built template into theme parts and copy assets.

        Returns:

        - `Path`: Absolute path to the created theme directory.

        """
        source_path = self.dist_dir / self.source_html
        if not source_path.is_file():
            msg = f"Source HTML not found: {source_path}"
            raise FileNotFoundError(msg)

        html = source_path.read_text(encoding="utf8")
        if MARKER_CONTENT_START not in html or MARKER_CONTENT_END not in html:
            msg = f"{source_path} has no h-ssg content markers. Rebuild Harrix-HTML-Template after adding SSG markers."
            raise ValueError(msg)

        optional_tags = self._extract_optional_tags(html)
        html_without_optional = html
        for tag_html in optional_tags.values():
            if tag_html:
                html_without_optional = html_without_optional.replace(tag_html, "", 1)

        parts = self._split_parts(html_without_optional)

        if self.theme_dir.exists():
            shutil.rmtree(self.theme_dir)
        parts_dir = self.theme_dir / "parts"
        optional_dir = parts_dir / "optional"
        optional_dir.mkdir(parents=True, exist_ok=True)

        for name, content in parts.items():
            (parts_dir / f"{name}.html").write_text(content, encoding="utf8")

        for name, tag_html in optional_tags.items():
            (optional_dir / f"{name}.html").write_text(
                tag_html.strip() + ("\n" if tag_html.strip() else ""), encoding="utf8"
            )

        self._copy_assets()

        manifest = {
            "source_html": self.source_html,
            "parts": list(parts.keys()),
            "optional": list(OPTIONAL_ASSET_PATTERNS.keys()),
            "asset_dirs": [name for name in ASSET_DIRS if (self.dist_dir / name).exists()],
            "placeholders": {
                "title": PLACEHOLDER_TITLE,
                "content": PLACEHOLDER_CONTENT,
                "optional_head": PLACEHOLDER_OPTIONAL_HEAD,
                "optional_scripts": PLACEHOLDER_OPTIONAL_SCRIPTS,
            },
        }
        (self.theme_dir / "manifest.json").write_text(
            json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
            encoding="utf8",
        )
        return self.theme_dir.resolve()

    @staticmethod
    def _between(text: str, start: str, end: str, *, include_markers: bool) -> str:
        """Return the substring between two markers."""
        if start not in text or end not in text:
            msg = f"Missing markers {start!r} / {end!r}"
            raise ValueError(msg)
        after_start = text.split(start, 1)[1]
        inner, _, _ = after_start.partition(end)
        if include_markers:
            return f"{start}{inner}{end}"
        return inner

    def _copy_assets(self) -> None:
        """Copy static asset directories from dist into the theme folder."""
        for name in ASSET_DIRS:
            src = self.dist_dir / name
            if src.is_dir():
                shutil.copytree(src, self.theme_dir / name)

    def _extract_optional_tags(self, html: str) -> dict[str, str]:
        """Find optional CSS/JS tags in the page HTML."""
        found: dict[str, str] = {}
        for name, pattern in OPTIONAL_ASSET_PATTERNS.items():
            match = pattern.search(html)
            found[name] = match.group(0) if match else ""
        return found

    def _split_parts(self, html: str) -> dict[str, str]:
        """Split page HTML into named theme parts with placeholders."""
        head_end = re.search(r"</head>", html, re.IGNORECASE)
        if head_end is None:
            msg = "HTML has no </head>"
            raise ValueError(msg)

        head = html[: head_end.end()]
        head = _TITLE_RE.sub(rf"\1{PLACEHOLDER_TITLE}\3", head, count=1)
        if MARKER_OPTIONAL_HEAD in head:
            head = head.replace(MARKER_OPTIONAL_HEAD, PLACEHOLDER_OPTIONAL_HEAD, 1)
        else:
            head = re.sub(r"</head>", f"{PLACEHOLDER_OPTIONAL_HEAD}\n  </head>", head, count=1, flags=re.IGNORECASE)

        rest = html[head_end.end() :]
        body_match = _BODY_OPEN_RE.search(rest)
        if body_match is None:
            msg = "HTML has no <body>"
            raise ValueError(msg)

        body_open = body_match.group(0)
        after_body = rest[body_match.end() :]

        chrome_header = self._between(
            after_body,
            MARKER_CHROME_HEADER_START,
            MARKER_CHROME_HEADER_END,
            include_markers=False,
        )
        after_header = after_body.split(MARKER_CHROME_HEADER_END, 1)[1]

        main_match = _MAIN_RE.search(after_header)
        if main_match is None:
            msg = "HTML has no <main>…</main>"
            raise ValueError(msg)
        main_html = main_match.group(0)
        if MARKER_CONTENT_START not in main_html or MARKER_CONTENT_END not in main_html:
            msg = "Main block has no content markers"
            raise ValueError(msg)
        before_content, _, remainder = main_html.partition(MARKER_CONTENT_START)
        _, _, after_content_marker = remainder.partition(MARKER_CONTENT_END)
        main = f"{before_content}{PLACEHOLDER_CONTENT}{after_content_marker}"

        after_main = after_header[main_match.end() :]
        chrome_footer = self._between(
            after_main,
            MARKER_CHROME_FOOTER_START,
            MARKER_CHROME_FOOTER_END,
            include_markers=False,
        )
        after_footer = after_main.split(MARKER_CHROME_FOOTER_END, 1)[1]

        if MARKER_OPTIONAL_SCRIPTS in after_footer:
            scripts_chunk = after_footer.replace(MARKER_OPTIONAL_SCRIPTS, PLACEHOLDER_OPTIONAL_SCRIPTS, 1)
        else:
            scripts_chunk = f"{PLACEHOLDER_OPTIONAL_SCRIPTS}\n{after_footer}"

        body_close = re.search(r"</body>\s*</html>\s*$", scripts_chunk, re.IGNORECASE)
        if body_close is None:
            msg = "HTML has no </body></html>"
            raise ValueError(msg)
        scripts = scripts_chunk[: body_close.start()].strip()
        if PLACEHOLDER_OPTIONAL_SCRIPTS not in scripts:
            scripts = f"{PLACEHOLDER_OPTIONAL_SCRIPTS}\n{scripts}".strip()
        document_end = scripts_chunk[body_close.start() :].strip() + "\n"

        return {
            "head": head.rstrip() + "\n",
            "body_open": body_open.rstrip() + "\n",
            "chrome_header": chrome_header.strip() + "\n",
            "main": main.strip() + "\n",
            "chrome_footer": chrome_footer.strip() + "\n",
            "scripts": scripts.strip() + "\n",
            "document_end": document_end,
        }

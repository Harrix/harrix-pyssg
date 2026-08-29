"""Render Marp presentation notes to HTML.

Tries Marp CLI (`npx @marp-team/marp-cli`) when Node is available. Falls back to
a slide split + markdown-it so the site still builds without Node.

"""

from __future__ import annotations

import re
import shutil
import subprocess
import tempfile
from pathlib import Path

from markdown_it import MarkdownIt
from mdit_py_plugins.dollarmath import dollarmath_plugin
from mdit_py_plugins.front_matter import front_matter_plugin
from mdit_py_plugins.tasklists import tasklists_plugin

_HR_RE = re.compile(r"^(\*{3,}|-{3,}|_{3,})\s*$")
_FENCE_RE = re.compile(r"^(`{3,}|~{3,})")
_TRUE = frozenset({"true", "yes", "on", "1"})


def is_marp_yaml(yaml_dict: dict | None) -> bool:
    """Return `True` when YAML enables a Marp presentation note."""
    data = yaml_dict or {}
    note_type = str(data.get("type") or "").strip().lower()
    if note_type == "marp":
        return True
    marp = data.get("marp")
    if marp is True:
        return True
    return str(marp or "").strip().lower() in _TRUE


def render_marp_html(md_path: Path, md_content: str) -> str:
    """Return a full HTML document for a Marp note."""
    cli_html = _render_with_marp_cli(md_path)
    if cli_html:
        return cli_html
    return _render_fallback_document(md_content)


def _render_fallback_document(md_content: str) -> str:
    md = (
        MarkdownIt("gfm-like", {"typographer": True, "linkify": False})
        .use(front_matter_plugin)
        .use(tasklists_plugin)
        .use(dollarmath_plugin)
        .enable(["replacements"])
    )
    slides = _split_slides(md_content)
    sections: list[str] = []
    for index, slide in enumerate(slides):
        body = md.render(slide).strip() or "<p></p>"
        active = " active" if index == 0 else ""
        sections.append(f'<section class="slide{active}" data-index="{index}">{body}</section>')
    inner = "\n".join(sections)
    return f"""<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8"/>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<title>Presentation</title>
<style>
html, body {{ margin: 0; height: 100%; background: #111; color: #222; font-family: system-ui, sans-serif; }}
.deck {{ height: 100%; display: flex; align-items: center; justify-content: center; }}
.stage {{
  width: min(100vw, calc(100vh * 16 / 9));
  aspect-ratio: 16 / 9;
  position: relative;
  overflow: hidden;
  background: #fff;
}}
.slide {{ position: absolute; inset: 0; display: none; padding: 5% 6%; overflow: auto; box-sizing: border-box; }}
.slide.active {{ display: block; }}
.slide img {{ max-width: 100%; height: auto; }}
.chrome {{ position: fixed; bottom: 12px; left: 0; right: 0; text-align: center; color: #eee; }}
</style>
</head>
<body>
<div class="deck"><div class="stage">{inner}</div></div>
<div class="chrome"><span id="counter"></span></div>
<script>
(function() {{
  var slides = document.querySelectorAll('.slide');
  var i = 0;
  function show(n) {{
    if (n < 0) n = 0;
    if (n > slides.length - 1) n = slides.length - 1;
    i = n;
    for (var s = 0; s < slides.length; s++) slides[s].classList.toggle('active', s === i);
    var c = document.getElementById('counter');
    if (c) c.textContent = (i + 1) + ' / ' + slides.length;
  }}
  document.addEventListener('keydown', function(e) {{
    if (e.key === 'ArrowRight' || e.key === ' ') show(i + 1);
    if (e.key === 'ArrowLeft') show(i - 1);
  }});
  document.addEventListener('click', function(e) {{
    if (e.clientX < window.innerWidth / 2) show(i - 1); else show(i + 1);
  }});
  show(0);
}})();
</script>
</body>
</html>
"""


def _render_with_marp_cli(md_path: Path) -> str | None:
    npx = shutil.which("npx") or shutil.which("npx.cmd")
    if npx is None or not md_path.is_file():
        return None
    with tempfile.TemporaryDirectory(prefix="hsg-marp-") as tmp:
        out = Path(tmp) / "index.html"
        cmd = [
            npx,
            "--yes",
            "@marp-team/marp-cli",
            str(md_path),
            "-o",
            str(out),
            "--no-stdin",
        ]
        try:
            completed = subprocess.run(
                cmd,
                check=False,
                capture_output=True,
                text=True,
                cwd=str(md_path.parent),
                timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired):
            return None
        if completed.returncode != 0 or not out.is_file():
            return None
        return out.read_text(encoding="utf-8")


def _split_slides(md_content: str) -> list[str]:
    text = md_content.lstrip("\ufeff")
    body = text
    if text.startswith("---"):
        end = text.find("\n---", 3)
        if end >= 0:
            rest = text[end + 4 :]
            body = rest.removeprefix("\n")
    slides: list[str] = []
    current: list[str] = []
    in_fence = False
    for line in body.splitlines():
        if _FENCE_RE.match(line.strip()):
            in_fence = not in_fence
            current.append(line)
            continue
        if not in_fence and _HR_RE.match(line.strip()):
            slides.append("\n".join(current).strip())
            current = []
            continue
        current.append(line)
    slides.append("\n".join(current).strip())
    return slides or [""]

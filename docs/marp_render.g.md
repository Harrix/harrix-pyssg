---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# 📄 File `marp_render.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🔧 Function `is_marp_yaml`](#-function-is_marp_yaml)
- [🔧 Function `render_marp_html`](#-function-render_marp_html)

</details>

## 🔧 Function `is_marp_yaml`

```python
def is_marp_yaml(yaml_dict: dict | None) -> bool
```

Return `True` when YAML enables a Marp presentation note.

<details>
<summary>Code:</summary>

```python
def is_marp_yaml(yaml_dict: dict | None) -> bool:
    data = yaml_dict or {}
    note_type = str(data.get("type") or "").strip().lower()
    if note_type == "marp":
        return True
    marp = data.get("marp")
    if marp is True:
        return True
    return str(marp or "").strip().lower() in _TRUE
```

</details>

## 🔧 Function `render_marp_html`

```python
def render_marp_html(md_path: Path, md_content: str) -> str
```

Return a full HTML document for a Marp note.

<details>
<summary>Code:</summary>

```python
def render_marp_html(md_path: Path, md_content: str) -> str:
    cli_html = _render_with_marp_cli(md_path)
    if cli_html:
        return cli_html
    return _render_fallback_document(md_content)
```

</details>

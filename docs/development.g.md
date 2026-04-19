---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# ⚙️ Development

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🚀 Deploy on an empty machine](#-deploy-on-an-empty-machine)
  - [📋 Prerequisites](#-prerequisites)
  - [📥 Installation steps](#-installation-steps)
- [💻 CLI commands](#-cli-commands)
- [➕ Adding a new function](#-adding-a-new-function)
- [👤 Author](#-author)

</details>

## 🚀 Deploy on an empty machine

### 📋 Prerequisites

Install the following software:

- Git
- Cursor or VSCode (with Python extensions)
- [uv](https://docs.astral.sh/uv/) ([Installing and Working with uv (Python) in VSCode](https://github.com/Harrix/harrix.dev-articles-2025-en/blob/main/uv-vscode-python/uv-vscode-python.md))

### 📥 Installation steps

1. Clone project:

   ```shell
   mkdir C:/GitHub
   cd C:/GitHub
   git clone https://github.com/Harrix/harrix-pyssg.git
   ```

2. Open the folder `C:/GitHub/harrix-pyssg` in Cursor (or VSCode).

3. Open a terminal `Ctrl` + `` ` ``.

4. Run `uv sync`.

## 💻 CLI commands

CLI commands after installation:

- `.venv\Scripts\Activate.ps1` — activate virtual environment
- `isort .` — sort imports.
- `ruff check --fix` — lint and fix the project's Python files.
- `ruff check` — lint the project's Python files.
- `ruff format` — format the project's Python files.
- `ty check` — check Python types in the project's Python files.
- `uv python install 3.13` + `uv python pin 3.13` + `uv sync` — switch to a different Python version.
- `uv self update` — update uv itself.
- `uv python upgrade` — upgrade python to the latest patch release.
- `uv sync --upgrade` — update all project libraries (sometimes you need to call twice).
- `vermin src` — determines the minimum version of Python. However, if the version is below 3.10, we stick with 3.10 because Python 3.10 annotations are used.
- `harrix-swiss-knife-cli python isort-ruff-sort-docs "D:/GitHub/harrix-pyssg"` — isort, ruff format, sort, make docs in PY files.

## ➕ Adding a new function

- Install [harrix-swiss-knife](https://github.com/Harrix/harrix-swiss-knife).
- Add the function in `src/harrix_pyssg/<module>.py`.
- Write a docstring in Markdown style.
- Add an example in Markdown style.
- Add a test in `tests/<module>.py`.
- Run `pytest`.
- Run `ty check`.
- Run `ruff check`.
- Check error messages in Cursor.
- From `harrix-swiss-knife`, call the command `Python` → `isort, ruff format, sort, make docs in PY files` and select folder `harrix-pyssg`.
- From `harrix-swiss-knife`, call the command `Python` → `Check PY in ...` and select folder `harrix-pyssg`.
- Create a commit `➕ Add function <function>()`.
- From `harrix-swiss-knife`, call the command `Python` → `Publish Python library to PyPI` and select folder `harrix-pyssg`.

## 👤 Author

Author: [Anton Sergienko](https://github.com/Harrix).

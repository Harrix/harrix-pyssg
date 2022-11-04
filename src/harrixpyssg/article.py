"""
## Usage examples

Generate an HTML file (and other related files) from Markdown with the full filename:

```python
md_filename = "C:/GitHub/harrix.dev/content/en/blog/2013/kbd-style/kbd-style.md"
html_folder = "C:/GitHub/harrix.dev/content/build_site"
hsg.Article(md_filename).generate_html(html_folder)
```

Generate an HTML file (and other related files) from Markdown with a relative path
to the file:

```python
md_filename = "./tests/data/test_01/test_01.md"
html_folder = "./build_site"
article = hsg.Article(md_filename)
article.generate_html(html_folder)
```

Generate HTML code from Markdown without creating files:

```python
md_filename = "./tests/data/test_01/test_01.md"
article = hsg.Article(md_filename)
print(article.html_code)
```

## Example of folder structure

Folder with the Markdown file:

```text
test_01
├─ test_01.md
├─ featured-image.png
└─ img
   └─ test-image.png
```

Output HTML folder:

```text
build_site
├─ featured-image.png
├─ img
│  └─ test-image.png
└─ index.html
```

Markdown file `test_01.md`:

```markdown
---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---

# Title

Hello, world!
```

HTML file `index.html`:

```html
<h1>Title</h1>
<p>Hello, world!</p>
```

# List of processed YAML tags

| Tag          | Description                                                                                                                                                                                         |
| ------------ | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `date`       | Date of creation of the article.                                                                                                                                                                    |
| `update`     | Date of the article update.                                                                                                                                                                         |
| `categories` | The list of categories to which the article belongs. Spaces in category names are not allowed.                                                                                                      |
| `tags`       | The list of tags to which the article belongs. Spaces in tags names are not allowed.                                                                                                                |
| `draft`      | `true` if the article is in drafts and should not be published. If the tag is not in YAML, the default value is false`.                                                                             |
| `latex`      | `true` if $LaTeX$ is used in the article. Example: `$y = x^{2}$`. If the tag is not in YAML, the default value is `false`.                                                                             |
| `related-id` | The key for linking several articles into a series of articles. If this parameter is present, then at the bottom of the article there will be a list of all articles with the same parameter value. |
| `demo`       |                                                                                                                                                                                                     |
| `download`   |                                                                                                                                                                                                     |
| `link`       |                                                                                                                                                                                                     |
| `source`     |                                                                                                                                                                                                     |

TODO

Example:

```yaml
date: 2022-09-18
update: 2022-09-19
categories: [it, web]
tags: [CSS, CSS-Grids]
draft: false
latex: true
related-id: html-lesson
```
"""
from __future__ import annotations

import re
import shutil
from pathlib import Path

import markdown

from .custom_logger import logger


class Article:
    """
    All information about one article from the site.

    Attributes:
    - `yaml_dict` (dict): List of article parameters from YAML. # TODO
    """

    def __init__(self, md_filename: str | Path):
        """
        Get all info of the Markdown file with folders.
        It does not generate new files and folders.

        Args:

        - `md_filename` (str | Path): Full filename of the Markdown file.
        """
        self._md_content = ""
        self._html_folder = Path()

        self.md_filename = Path(md_filename)
        # Follow @md_filename.setter

    @property
    def md_filename(self):
        """
        `str | Path`: Full filename of the Markdown file.
        Example: `"./tests/data/test_01/test_01.md"`.
        """
        return self._md_filename

    @md_filename.setter
    def md_filename(self, new_value: str | Path):
        self._md_filename = Path(new_value)
        try:
            self.md_content = Path(self.md_filename).read_text(encoding="utf8")
        except:
            logger.error(f'The file "{new_value}" does not open')
        # Follow @md_filename.md_content

    @property
    def md_content(self):
        """
        `str`: The contents of the Markdown file. Example:

        ```markdown
        ---
        date: 2022-09-18
        categories: [it, web]
        tags: [CSS]
        ---

        # Title

        Hello, world!
        ```
        """
        return self._md_content

    @md_content.setter
    def md_content(self, new_value: str):
        self._md_content = new_value

    @property
    def md_without_yaml(self):
        """
        `str`: Text of the article in the form of Markdown without YAML text. Example:

        ```md
        # Title

        Hello, world!
        ```
        """
        return re.sub(r"^---(.|\n)*?---\n", "", self.md_content.lstrip()).lstrip()

    @md_without_yaml.setter
    def md_without_yaml(self, new_value: str):
        self.md_content = f"{self.md_yaml}\n\n{new_value}"

    @property
    def md_yaml(self):
        """
        `str`: YAML from the Markdown file. Example:

        ```yaml
        ---
        date: 2022-09-18
        categories: [it, web]
        tags: [CSS]
        ---
        ```
        """
        find = re.search(r"^---(.|\n)*?---\n", self.md_content.lstrip(), re.DOTALL)
        if find:
            return find.group().rstrip()
        return ""

    @md_yaml.setter
    def md_yaml(self, new_value: str):
        self.md_content = f"{new_value.lstrip()}\n\n{self.md_without_yaml}"

    @property
    def html_code(self):
        """
        `str`: HTML clean code from the Markdown code (only getter). Example:

        ```html
        <h1>Title</h1>
        <p>Hello, world!</p>
        ```
        """
        md_engine = markdown.Markdown()
        return md_engine.convert(self.md_without_yaml)

    @property
    def html_folder(self):
        """
        `Path`: Output folder of HTML file. Example: `./build_site`.
        """
        return self._html_folder

    @html_folder.setter
    def html_folder(self, new_value: Path):
        self._html_folder = new_value

    @property
    def html_filename(self):
        """
        `Path`: Output filename of HTML file (only getter).
        Example: `./build_site/index.html`.
        """
        return self.html_folder / "index.html"

    @property
    def featured_image_filenames(self):
        """
        `list[str]`: Array of featured images. The files must be in the same folder
        as the Markdown file. Example: `["featured-image.png", "featured-image.svg"]`.
        """
        res = []
        for file in self.md_filename.parent.iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                res.append(file.name)
        return res

    def generate_html(self, html_folder: str | Path) -> Article:
        """
        Generate HTML file with folders from the Markdown file with folders.

        Args:

        - `html_folder` (str | Path): Output folder of the HTML file.

        Returns:

        - `Article`: Returns itself, that is, the article with calculated data.
        """
        self.html_folder = Path(html_folder)

        self._clear_html_folder_directory()
        self._copy_dirs()
        self._copy_featured_images()

        self.html_filename.write_text(self.html_code, encoding="utf8")
        return self

    def _clear_html_folder_directory(self) -> None:
        """
        This method clears `self.html_folder` with sub-directories.
        """
        shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)

    def _copy_dirs(self) -> None:
        """
        This method copies all folders from the directory with the Markdown file.
        """
        for file in Path(self.md_filename).parent.iterdir():
            if file.is_dir():
                shutil.copytree(file, self.html_folder / file.name, dirs_exist_ok=True)

    def _copy_featured_images(self) -> None:
        """
        This method copies all featured images from the directory with the Markdown file.
        """
        for filename in self.featured_image_filenames:
            file = self.md_filename.parent / filename
            output_file = self.html_folder / filename
            shutil.copy(file, output_file)

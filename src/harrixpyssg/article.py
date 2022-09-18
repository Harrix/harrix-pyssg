"""
## Usage examples

```python
md_filename = "C:/GitHub/harrix.dev/content/en/blog/2013/kbd-style/kbd-style.md"
html_folder = "C:/GitHub/harrix.dev/content/build_site"
hsg.Article(md_filename).generate_html(html_folder)
```

```python
md_filename = "./tests/data/test/test.md"
html_folder = "./build_site"
article = hsg.Article(md_filename)
article.generate_html(html_folder)
```

```python
md_filename = "./tests/data/test/test.md"
article = hsg.Article(md_filename)
print(article.html_code)
```

## Example of folder structure

Folder with the Markdown file:

```text
test
├─ test.md
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

Markdown file `test.md`:

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

- `date`: Date of creation of the article.
- `update`: Date of the article update.
- `categories`: The list of categories to which the article belongs.
  Spaces in category names are not allowed.
- `tags`: The list of tags to which the article belongs.
  Spaces in tags names are not allowed.
- `draft`: `true` if the article is in drafts and should not be published.
  If the tag is not in YAML, the default value is `false`.
- `latex`: `true` if LaTeX is used in the article. Example: `$y = x^{2}$`
  If the tag is not in YAML, the default value is `false`.
- `related-id`: The key for linking several articles into a series of articles.
  If this parameter is present, then at the bottom of the article there will be a list
  of all articles with the same parameter value.
- `demo`: .
- `download`: .
- `link`: .
- `source`: .

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


class Article:
    """
    All information about one article from the site.

    Attributes:

    - `md_filename` (Path): Full filename of the Markdown file.
      Example: `"./tests/data/test/test.md"`.
    - `md_without_yaml` (str): Text of the article in the form of Markdown without YAML
      text. Example:

      ```md
      # Title

      Hello, world!
      ```
    - `md_yaml` (str): YAML from the Markdown file. Example:

      ```yaml
      ---
      date: 2022-09-18
      categories: [it, web]
      tags: [CSS]
      ---
      ```

    - `html_code` (str): HTML clean code from the Markdown code. Example:

      ```html
      <h1>Title</h1>
      <p>Hello, world!</p>
      ```

    - `featured_image_filenames` (list[str]): Array of featured images. The files must
      be in the same folder as the Markdown file.
      Example: `["featured-image.png", "featured-image.svg"]`.
    - `yaml_dict` (dict): List of article parameters from YAML.
    - `html_folder` (Path): Output folder of HTML file.
      Example: `./build_site`.
    - `html_filename` (Path): Output folder of HTML file.
      Example: `./build_site/index.html`.
    """

    def __init__(self, md_filename: str | Path):
        """
        Get all info of the Markdown file with folders.
        It does not generate new files and folders.

        Args:

        - `md_filename` (str | Path): Full filename of the Markdown file.
        """
        self.md_filename = Path(md_filename)

        md = Path(self.md_filename).read_text(encoding="utf8")
        md_engine = markdown.Markdown(extensions=["meta"])

        self.md_without_yaml = self.__remove_yaml_from_markdown(md)
        self.md_yaml = self.__get_yaml_from_markdown(md)
        self.html_code = md_engine.convert(md)
        self.featured_image_filenames = self.__get_featured_image_filenames()

        self.html_folder = Path()
        self.html_filename = Path()

        self.yaml_dict = self.__process_meta(md_engine)

    def generate_html(self, html_folder: str | Path) -> Article:
        """
        Generate HTML file with folders from the Markdown file with folders.

        Args:

        - `html_folder` (str | Path): Output folder of the HTML file.

        Returns:

        - `Article`: Returns itself, that is, the article with calculated data.
        """

        self.html_folder = Path(html_folder)
        self.html_filename = self.html_folder / "index.html"

        self.__clear_html_folder_directory()
        self.__copy_dirs()
        self.__copy_featured_images()

        self.html_filename.write_text(self.html_code, encoding="utf8")
        return self

    def __process_meta(self, md_engine):
        """
        This method removes YAML from text of the Markdown file.
        """
        res = dict()

        return res

    def __remove_yaml_from_markdown(self, md_text: str) -> str:
        """
        This method removes YAML from text of the Markdown file.
        """
        return re.sub(r"^---(.|\n)*?---\n", "", md_text.lstrip()).lstrip()

    def __get_yaml_from_markdown(self, md_text: str) -> str:
        """
        This method gets YAML from text of the Markdown file.
        """
        find = re.search(r"^---(.|\n)*?---\n", md_text.lstrip(), re.DOTALL)
        if find:
            return find.group().rstrip()
        return ""

    def __get_featured_image_filenames(self) -> list:
        """
        This method returns list of featured images filenames.
        The Markdown and `featured-image.*`` files must be in the same folder.
        """
        res = []
        for file in self.md_filename.parent.iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                res.append(file.name)
        return res

    def __clear_html_folder_directory(self) -> None:
        """
        This method clears `self.html_folder` with sub-directories.
        """
        shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)

    def __copy_dirs(self) -> None:
        """
        This method copies all folders from the directory with the Markdown file.
        """
        for file in Path(self.md_filename).parent.iterdir():
            if file.is_dir():
                shutil.copytree(file, self.html_folder / file.name, dirs_exist_ok=True)

    def __copy_featured_images(self) -> None:
        """
        This method copies all featured images from the directory with the Markdown file.
        """
        for file in Path(self.md_filename.parent).iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                output = self.html_folder / file.name
                shutil.copy(file, output)
                self.featured_image_filenames.append(output.name)

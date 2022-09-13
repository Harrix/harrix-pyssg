"""
## Usage examples

```python
md_filename = "./tests/data/test/test.md"
html_folder = "./build_site"
a = hsg.Article(md_filename).generate_from_md(html_folder)
```

```python
md_filename = "./tests/data/test/test.md"
a = hsg.Article(md_filename)
print(a.html_code)
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
date: 2022-09-13
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
"""
import shutil
from pathlib import Path
import markdown
import re


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
      date: 2022-09-13
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

        self.__meta = md_engine.Meta  # TODO

    def generate_from_md(self, html_folder: str | Path):
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

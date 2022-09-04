"""
## Structure of the article

```text
data\2022-01-04-test-article
├─ 2022-01-04-test-article.md
├─ featured-image.png
└─ img
   └─ test-image.png
```

## Usage example

```python
md_filename = "./tests/data/2022-01-04-test/2022-01-04-test.md"
html_folder = "./build_site"
a = hsg.Article().generate_from_md(md_filename, html_folder)
```
"""
import shutil
from pathlib import Path
import markdown

import harrixpylib as h


class Article:
    """
    All information about one article from the site.

    Attributes:

    - `md_filename` (Path): Full filename of the Markdown file.
      Example: `"./tests/data/2022-01-04-test/2022-01-04-test.md"`.
    - `md_without_yaml` (str): Text of the article in the form of Markdown without YAML
      text. Example:

      ```md
      # Title

      Hello, world!
      ```
    - `md_yaml` (str): YAML from thу Markdown file. Example:

      ```md
      ---
      categories: [it, web]
      tags: [CSS]
      ---
      ```

    - `html_folder` (Path): Output folder of HTML file.
      Example: `./build_site`.
    - `html_filename` (Path): Output folder of HTML file.
      Example: `./build_site/index.html`.
    - `html_code` (str): HTML clean code from the Markdown code. Example:

      ```html
      <h1>Title</h1>
      <p>Hello, world!</p>
      ```

    - `featured_image_filenames` (list(str)): Array of featured images. The files must
      be in the same folder as the Markdown file.
      Example: `["featured-image.png", "featured-image.svg"]`.
    """

    def __init__(self):
        self.md_filename = Path()
        self.md_without_yaml = ""
        self.md_yaml = ""
        self.html_folder = Path()
        self.html_filename = Path()
        self.html_code = ""
        self.featured_image_filenames = []
        self.__meta = dict()  # TODO

    def generate_from_md(self, md_filename: str, html_folder: str):
        """
        Generate HTML file with folders from the Markdown file with folders.

        Args:

        - `md_filename` (str): Full filename of the Markdown file.
        - `html_folder` (str): Output folder of the HTML file.

        Returns:

        - `Article`: Returns itself, that is, the article with calculated data.
        """
        self.get_info(md_filename, html_folder)

        h.clear_directory(self.html_folder)
        self.__copy_dirs()
        self.__copy_featured_images()

        self.html_filename.write_text(self.html_code, encoding="utf8")
        return self

    def get_info(self, md_filename: str, html_folder: str):
        """
        Get all info of the Markdown file with folders. The method is used in the method
        `generate_from_md()`. It does not generate new files and folders.

        Args:

        - `md_filename` (str): Full filename of the Markdown file.
        - `html_folder` (str): Output folder of the HTML file.

        Returns:

        - `Article`: Returns itself, that is, the article with calculated data.
        """
        self.md_filename = Path(md_filename)
        self.html_folder = Path(html_folder)

        md = Path(self.md_filename).read_text(encoding="utf8")

        md_engine = markdown.Markdown(extensions=["meta"])

        self.html_code = md_engine.convert(md)
        self.html_filename = self.html_folder / "index.html"
        self.md_without_yaml = h.remove_yaml_from_markdown(md)
        self.md_yaml = h.get_yaml_from_markdown(md)
        self.__meta = md_engine.Meta  # TODO
        return self

    def __copy_dirs(self):
        """
        Copies all folders from the directory with the Markdown file.
        """
        for file in Path(self.md_filename).parent.iterdir():
            if file.is_dir():
                shutil.copytree(file, self.html_folder / file.name, dirs_exist_ok=True)

    def __copy_featured_images(self):
        """
        Copies all featured images from the directory with the Markdown file.
        """
        for file in Path(self.md_filename.parent).iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                output = self.html_folder / file.name
                shutil.copy(file, output)
                self.featured_image_filenames.append(output.name)


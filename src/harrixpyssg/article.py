"""
## Usage example

```py
markdown_filename = './tests/data/2022-01-04-test-article/2022-01-04-test-article.md'
output_path = './build_site'
a = hsg.Article().generate_from_md(markdown_filename, output_path)
```
"""
import shutil
from pathlib import Path
import markdown

import harrixpylib as h


class Article:
    """All information about one article from the site."""

    def __init__(self):
        self.markdown_filename:str = None
        """Full filename of Markdown file. Example:

        ```py
        './tests/data/2022-01-04-test-article/2022-01-04-test-article.md'
        ```
        """
        self.markdown_code:str = None
        """The text of the article in the form of Markdown without YAML text. Example:

        ```md
        # Title

        Hello, world!
        ```
        """
        self.html_output_folder = None
        """Output folder for HTML file. Example:

        ```py
        './build_site'
        ```
        """
        self.featured_image_filenames = []
        """Array of featured images. The files must be in the same folder as the markdown file. Example:

        ```py
        ['featured-image.png', 'featured-image.svg']
        ```
        """
        self.attribution_filename = None
        """The filename with attribution data. Example:

        ```py

        ```
        """
        self.html_filename = None
        """ Example:

        ```py

        ```
        """
        self.html_code = None
        """HTML clean code from Markdown code. Example:

        ```html
        <h1>Title</h1>
        <p>Hello, world!</p>
        ```
        """
        self.permalink = None
        """ Example:

        ```py

        ```
        """

        self.__meta = dict()

    def generate_from_md(self, markdown_filename: str, html_output_folder: str):
        """Generate HTML file with folders from markdown file with folders.

        Args:
            markdown_filename (str): [description]
            html_output_folder (str): [description]

        Returns:
            [type]: [description]
        """
        self.markdown_filename = Path(markdown_filename)
        self.html_output_folder = Path(html_output_folder)

        markdown_text = h.open_file(self.markdown_filename)

        md_engine = markdown.Markdown(extensions=["meta"])
        self.html_code = md_engine.convert(markdown_text)
        self.html_filename = self.html_output_folder / "index.html"
        self.__meta = md_engine.Meta
        self.markdown_code = h.remove_yaml_from_markdown(markdown_text)

        h.clear_directory(self.html_output_folder)
        self.__copy_dirs()
        self.__copy_featured_image()
        self.__copy_attribution()
        h.save_file(self.html_code, self.html_filename)
        return self

    def __copy_dirs(self):
        for file in Path(self.markdown_filename.parent).iterdir():
            if file.is_dir():
                shutil.copytree(file, self.html_output_folder / file.name, dirs_exist_ok=True)

    def __copy_featured_image(self):
        for file in Path(self.markdown_filename.parent).iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                output = self.html_output_folder / file.name
                shutil.copy(file, output)
                self.featured_image_filenames.append(output.name)

    def __copy_attribution(self):
        filename = "attribution.json"
        file = Path(self.markdown_filename.parent / filename)
        if file.is_file():
            output = self.html_output_folder / filename
            shutil.copy(file, output)
            self.attribution_filename = filename

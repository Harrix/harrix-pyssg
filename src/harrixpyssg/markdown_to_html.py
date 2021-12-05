from pathlib import Path
import shutil
import markdown

from .article import Article

import harrixpylib as h


class MarkdownToHtml:
    def __init__(self, markdown_filename, output_path):
        self.markdown_filename = Path(markdown_filename)
        self.output_path = Path(output_path)
        self.article = Article()

    def start(self):
        h.clear_directory(self.output_path)

        markdown_text = h.open_file(self.markdown_filename)

        md = markdown.Markdown(extensions=["meta"])
        html = md.convert(markdown_text)
        path_html = self.output_path / "index.html"
        self.article.meta = md.Meta
        self.article.md = h.remove_yaml_from_markdown(markdown_text)
        self.article.path_html = path_html
        self.article.html = html

        self.copy_dirs()
        self.copy_featured_image()
        self.copy_attribution()

        h.save_file(html, self.output_path / "index.html")

    def copy_dirs(self):
        for file in Path(self.markdown_filename.parent).iterdir():
            if file.is_dir():
                shutil.copytree(file, self.output_path / file.name, dirs_exist_ok=True)

    def copy_featured_image(self):
        self.article.featured_image = []
        for file in Path(self.markdown_filename.parent).iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                output = self.output_path / file.name
                shutil.copy(file, output)
                self.article.featured_image.append(output.name)

    def copy_attribution(self):
        self.article.attribution = False
        file = Path(self.markdown_filename.parent / "attribution.json")
        if file.is_file():
            output = self.output_path / "attribution.json"
            shutil.copy(file, output)
            self.article.attribution = "attribution.json"

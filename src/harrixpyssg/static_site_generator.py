from pathlib import Path
import re

from .article import Article
import harrixpylib as h


class StaticSiteGenerator:
    def __init__(self, md_paths, output_folder):
        self.md_folders = [Path(p).resolve() for p in md_paths]
        self.output_folder = Path(output_folder)
        self.articles = list()
        self.is_md_filename_analysis = True
        self.base_lang = "ru"

    def start(self):
        h.clear_directory(self.output_folder)
        self.generate_articles()
        for article in self.articles:
            # print(article.path_html)
            h.log.info(article.path_html)
        return self

    def generate_articles(self, is_clear_output_folder=False):
        if is_clear_output_folder:
            h.clear_directory(self.output_folder)
        for md_folder in self.md_folders:
            for item in md_folder.rglob("*.md"):
                parts = list(item.parts[len(md_folder.parts) : :])
                h.log.info(parts)

                if self.is_md_filename_analysis:
                    stem = item.stem
                    pattern1 = r"^(\d{4})-(\d{2})-(\d{2})-(.*?)\.(\w{2})$"
                    pattern2 = r"^(\d{4})-(\d{2})-(\d{2})-(.*?)$"
                    search1 = re.findall(pattern1, stem)
                    search2 = re.findall(pattern2, stem)
                    if search1:
                        parts2 = [search1[0][-2], search1[0][-1]]
                    elif search2:
                        parts2 = [search2[0][-1], self.base_lang]
                    h.log.info("parts2 = " + str(parts2))

                html_output_folder = self.output_folder / parts[0]
                a = Article().generate_from_md(item, html_output_folder)
                self.articles.append(a)
            h.log.info(md_folder)
        return self

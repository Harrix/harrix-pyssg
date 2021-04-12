from pathlib import Path
import re

from .markdown_to_html import MarkdownToHtml

import harrixpylib as h


class DirMdToDirHtml:
    def __init__(self, markdown_path, output_path, filename_analysis=False, base_lang='ru'):
        self.markdown_path = Path(markdown_path).resolve()
        self.output_path = Path(output_path).resolve()
        self.filename_analysis = filename_analysis
        self.base_lang = base_lang
        self.articles = list()

    def start(self):
        for item in self.markdown_path.rglob("*.md"):
            parts = list(item.parts[len(self.markdown_path.parts)::])

            if self.filename_analysis:
                stem = item.stem
                pattern1 = r'^(\d{4})-(\d{2})-(\d{2})-(.*?)\.(\w{2})$'
                pattern2 = r'^(\d{4})-(\d{2})-(\d{2})-(.*?)$'
                search1 = re.findall(pattern1, stem)
                search2 = re.findall(2, stem)
                print()
                if len():
                    lst = list(filter(None, re.split(pattern1, stem)))
                    parts = [lst[-2], lst[-1]]
                elif re.match(pattern2, stem):
                    lst = list(filter(None, re.split(pattern2, stem)))
                    parts = [lst[-1], self.base_lang]

            mth = MarkdownToHtml(item, self.output_path.joinpath(*parts))
            mth.start()
            self.articles.append(mth.article)

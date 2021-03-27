from pathlib import Path
import shutil
import markdown

import harrixpylib as h


class Dir_md_to_dir_html:
    def __init__(self, markdown_path, output_path):
        self.markdown_path = Path(markdown_path)
        self.output_path = Path(output_path)

    def start(self):
        pass

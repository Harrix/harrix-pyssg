import os
from pathlib import Path
import shutil
import markdown


def path_to_pathlib(path):
    if isinstance(path, str):
        return Path(path)
    return path


def clear_directory(path):
    """
    This function clear directory with sub-directories
    :param path: path of directory from pathlib
    """
    path = path_to_pathlib(path)
    if path.is_dir():
        shutil.rmtree(path)  # Remove folder
    path.mkdir(parents=True, exist_ok=True)  # Add folder


def open_file(filename):
    filename = path_to_pathlib(filename)
    s = ""
    with open(filename, 'r', encoding='utf8') as file:
        s = file.read()
    return s


def save_file(text, filename):
    filename = path_to_pathlib(filename)
    with open(filename, 'w', encoding='utf8') as file:
        file.write(text)


class HarrixMarkdownToHtml:
    def __init__(self, markdown_filename, output_path):
        self.markdown_filename = Path(markdown_filename)
        self.output_path = Path(output_path)

        clear_directory(self.output_path)

        self.copy_dirs()

        markdown_text = open_file(self.markdown_filename)

        html = markdown.markdown(markdown_text)

        save_file(html, self.output_path / 'output.html')

    def copy_dirs(self):
        dirs_of_files = ['img', 'files', 'demo', 'gallery']
        for d in dirs_of_files:
            self.copy_dir(d)

    def copy_dir(self, directory):
        path_img = self.markdown_filename.parent / directory
        if path_img.is_dir():
            shutil.copytree(path_img, self.output_path / directory, dirs_exist_ok=True)

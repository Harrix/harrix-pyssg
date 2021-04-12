import os, sys
from pathlib import Path
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

import harrixpyssg as hsg


def main():
    # markdown_filename = 'C:/Harrix/GitHub/harrix.dev-blog-2019/2019-07-23-add-2-num-android/2019-07-23-add-2-num-android.md'
    # output_path = '../dist'
    # hsg.MarkdownToHtml(markdown_filename, output_path).start()

    markdown_path = 'C:/Harrix/GitHub/harrix.dev-blog-2017/'
    # output_path = './dist'
    # hsg.Dir_md_to_dir_html(markdown_path, output_path).start()
    path = Path('C:\\Harrix\\GitHub\harrix.dev\\src\\_posts\\blog\\2013\\2013-01-03-log-of-base-two-in-mathcad\\2013-01-03-log-of-base-two-in-mathcad.en.md').resolve()
    print(path.parents[1])


if __name__ == '__main__':
    main()

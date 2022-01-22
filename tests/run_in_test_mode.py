from pathlib import Path
import harrixpylib as h

import harrixpyssg as hsg


def main():
    md_filename = './tests/data/2022-01-04-test-article/2022-01-04-test-article.md'
    html_output_folder = './build_site'
    a = hsg.Article().generate_from_md(md_filename, html_output_folder)

    # markdown_path = "C:/GitHub/harrix.dev-blog-2017/"
    # output_path = './build_site'
    # hsg.DirMdToDirHtml(markdown_path, output_path).start()


if __name__ == "__main__":
    main()

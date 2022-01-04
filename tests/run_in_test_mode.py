from pathlib import Path
import harrixpylib as h

import harrixpyssg as hsg


def main():
    markdown_filename = './tests/data/2022-01-04-test-article/2022-01-04-test-article.md'
    output_path = './build_site'
    a = hsg.Article().generate_from_markdown(markdown_filename, output_path)

    # markdown_path = "C:/GitHub/harrix.dev-blog-2017/"
    # output_path = './build_site'
    # hsg.DirMdToDirHtml(markdown_path, output_path).start()


if __name__ == "__main__":
    main()

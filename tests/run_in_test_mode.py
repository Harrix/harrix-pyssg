from pathlib import Path
import harrixpylib as h

import harrixpyssg as hsg


def main():
    ...
    md_filename = "./tests/data/2022-01-04-test/2022-01-04-test.md"
    html_output_folder = "./build_site"
    a = hsg.Article().generate_from_md(md_filename, html_output_folder)

    # md_filename = './tests/data/2022-01-04-test/2022-01-04-test.md'
    # html_output_folder = './build_site'
    # a = hsg.Article().generate_from_md(md_filename, html_output_folder)

    # md_folders = ["C:/GitHub/harrix.dev-blog-2017/"]
    # output_folder = './build_site'
    # hsg.StaticSiteGenerator(md_folders, output_folder).generate_articles()


if __name__ == "__main__":
    main()

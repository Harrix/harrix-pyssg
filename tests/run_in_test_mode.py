from pathlib import Path

import harrixpyssg as hsg


def main():
    ...
    md_filename = "./tests/data/test/test.md"
    html_folder = "./build_site"
    a = hsg.Article(md_filename).generate_from_md(html_folder)
    # md_folders = ["C:/GitHub/harrix.dev-blog-2017/"]
    # output_folder = './build_site'
    # hsg.StaticSiteGenerator(md_folders, output_folder).generate_articles()


if __name__ == "__main__":
    main()

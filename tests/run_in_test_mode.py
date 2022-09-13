from pathlib import Path

import harrixpyssg as hsg


def main():
    ...
    # md_filename = "./tests/data/test/test.md"
    # html_folder = "./build_site"
    # a = hsg.Article(md_filename).generate_html(html_folder)
    md_folder = "./tests/data"
    # md_folder = "C:/GitHub/harrix.dev/content"
    html_folder = "./build_site"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.generate_site(html_folder)


if __name__ == "__main__":
    main()

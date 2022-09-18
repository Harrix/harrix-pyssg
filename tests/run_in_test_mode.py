from pathlib import Path

import harrixpyssg as hsg




def main():
    ...
    # run_test_article()
    run_test_static_site_generator()
    # run_get_yaml_tags

def run_test_static_site_generator():
    md_folder = "C:/GitHub/harrix.dev/content"
    html_folder = "./build_site"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.generate_site(html_folder)


def run_test_article():
    md_filename = "./tests/data/test/test.md"
    html_folder = "./build_site"
    hsg.Article(md_filename).generate_html(html_folder)


def run_get_yaml_tags():
    md_folder = "C:/GitHub/harrix.dev/content"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.get_yaml()


if __name__ == "__main__":
    main()

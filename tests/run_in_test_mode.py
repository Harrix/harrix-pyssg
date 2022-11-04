import datetime
from pathlib import Path

import harrixpyssg as hsg


def main():
    ...
    # run_test()
    # run_test_article()
    # run_test_article_test_03()
    # run_test_article_md_content()
    run_test_article_md_yaml()
    # run_test_static_site_generator()
    # run_get_yaml_tags()


def run_test():
    ...


def run_test_article():
    md_filename = "./tests/data/test_01/test_01.md"
    html_folder = "./build_site"
    hsg.Article(md_filename).generate_html(html_folder)


def run_test_article_test_03():
    md_filename = "./tests/data/test_03/test_03.md"
    html_folder = "./build_site"
    hsg.Article(md_filename).generate_html(html_folder)


def run_test_article_md_content():
    md_filename = "./tests/data/test_01/test_01.md"
    a = hsg.Article(md_filename)
    print(a.md_content)


def run_test_article_md_yaml():
    md_filename = "./tests/data/test_01/test_01.md"
    a = hsg.Article(md_filename)
    print(a.md_yaml)
    print(a.md_yaml_dict)
    a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
    print(a.md_yaml)


def run_test_static_site_generator():
    # md_folder = "C:/GitHub/harrix.dev/content"
    md_folder = "./tests/data"
    html_folder = "./build_site"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.generate_site(html_folder)


def run_get_yaml_tags():
    md_folder = "C:/GitHub/harrix.dev/content"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.get_yaml()


if __name__ == "__main__":
    main()

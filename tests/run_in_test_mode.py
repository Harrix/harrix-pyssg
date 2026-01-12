"""Test runner script for manual testing of harrix_pyssg functionality."""

import datetime
from pathlib import Path

import harrix_pyssg as hsg


def main() -> None:
    run_test()


def run_test() -> None:
    if True:
        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_generalized_md()


def run_test_add_yaml_tag_to_all_md() -> None:
    md_folder = "./tests/data"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.add_yaml_tag_to_all_md(("author", "Anton Sergienko"))


def run_test_article() -> None:
    md_filename = "./tests/data/test_01/test_01.md"
    html_folder = "./build_site"
    hsg.Article(md_filename).generate_html(html_folder)


def run_test_article_get_nocode_code_parts() -> None:
    md_filename = "./tests/data/test_03/test_03.md"
    a = hsg.Article(md_filename)
    print(*a._get_nocode_code_parts(), sep="\n")
    print("\n".join(x[0] for x in a._get_nocode_code_parts()))


def run_test_article_md_content() -> None:
    md_filename = "./tests/data/test_01/test_01.md"
    a = hsg.Article(md_filename)
    print(a.md_content)


def run_test_article_md_save() -> None:
    md_filename = "./tests/data/test_01/test_01.md"
    a = hsg.Article(md_filename)
    a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
    a.md_content_no_yaml = "# New title\n\nNew content"
    a.save()  # Be careful!
    new_content = Path(md_filename).read_text(encoding="utf8").lstrip()
    print(new_content)


def run_test_article_md_yaml() -> None:
    md_filename = "./tests/data/test_01/test_01.md"
    a = hsg.Article(md_filename)
    a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
    print(a.md_content)


def run_test_article_test_03() -> None:
    md_filename = "./tests/data/test_03/test_03.md"
    html_folder = "./build_site"
    hsg.Article(md_filename).generate_html(html_folder)


def run_test_get_set_variables_from_yaml() -> None:
    md_folder = "./tests/data"
    sg = hsg.StaticSiteGenerator(md_folder)
    print(sg.get_set_variables_from_yaml())


def run_test_static_site_generator() -> None:
    md_folder = "./tests/data"
    html_folder = "./build_site"
    sg = hsg.StaticSiteGenerator(md_folder)
    sg.generate_site(html_folder)


def run_test_static_site_generator_save() -> None:
    md_folder = "C:/GitHub/_content__harrix-dev"
    sg = hsg.StaticSiteGenerator(md_folder)
    for a in sg.articles:
        a.save()


if __name__ == "__main__":
    main()

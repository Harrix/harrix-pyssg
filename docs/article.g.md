# 📄 File `article.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🏛️ Class `Article`](#%EF%B8%8F-class-article)
- [Usage examples](#usage-examples)
- [Example of folder structure](#example-of-folder-structure)
  - [⚙️ Method `__init__`](#%EF%B8%8F-method-__init__)
  - [⚙️ Method `add_image_captions`](#%EF%B8%8F-method-add_image_captions)
  - [⚙️ Method `featured_image_filenames`](#%EF%B8%8F-method-featured_image_filenames)
  - [⚙️ Method `generate_html`](#%EF%B8%8F-method-generate_html)
  - [⚙️ Method `html_code`](#%EF%B8%8F-method-html_code)
  - [⚙️ Method `html_filename`](#%EF%B8%8F-method-html_filename)
  - [⚙️ Method `html_folder`](#%EF%B8%8F-method-html_folder)
  - [⚙️ Method `html_folder`](#%EF%B8%8F-method-html_folder-1)
  - [⚙️ Method `load`](#%EF%B8%8F-method-load)
  - [⚙️ Method `md_content`](#%EF%B8%8F-method-md_content)
  - [⚙️ Method `md_content_no_yaml`](#%EF%B8%8F-method-md_content_no_yaml)
  - [⚙️ Method `md_content_no_yaml`](#%EF%B8%8F-method-md_content_no_yaml-1)
  - [⚙️ Method `md_filename`](#%EF%B8%8F-method-md_filename)
  - [⚙️ Method `md_yaml`](#%EF%B8%8F-method-md_yaml)
  - [⚙️ Method `md_yaml_dict`](#%EF%B8%8F-method-md_yaml_dict)
  - [⚙️ Method `save`](#%EF%B8%8F-method-save)
  - [⚙️ Method `to_sub_article`](#%EF%B8%8F-method-to_sub_article)
  - [⚙️ Method `_clear_html_folder_directory`](#%EF%B8%8F-method-_clear_html_folder_directory)
  - [⚙️ Method `_copy_dirs`](#%EF%B8%8F-method-_copy_dirs)
  - [⚙️ Method `_copy_featured_images`](#%EF%B8%8F-method-_copy_featured_images)
  - [⚙️ Method `_get_nocode_code_parts`](#%EF%B8%8F-method-_get_nocode_code_parts)
  - [⚙️ Method `_process_no_code_content`](#%EF%B8%8F-method-_process_no_code_content)

</details>

## 🏛️ Class `Article`

```python
class Article
```

All information about one article from the site.

## Usage examples

Generate an HTML file (and other related files) from Markdown with the full filename:

```python
import harrixpyssg as hsg

md_filename = "C:/GitHub/harrix.dev/content/en/blog/2013/kbd-style/kbd-style.md"
html_folder = "C:/GitHub/harrix.dev/content/build_site"
hsg.Article(md_filename).generate_html(html_folder)
```

Generate an HTML file (and other related files) from Markdown with a relative path
to the file:

```python
import harrixpyssg as hsg

md_filename = "./tests/data/test_01/test_01.md"
html_folder = "./build_site"
article = hsg.Article(md_filename)
article.generate_html(html_folder)
```

Generate HTML code from Markdown without creating files:

```python
import harrixpyssg as hsg

md_filename = "./tests/data/test_01/test_01.md"
article = hsg.Article(md_filename)
print(article.html_code)
```

## Example of folder structure

Folder with the Markdown file:

```text
test_01
├─ test_01.md
├─ featured-image.png
└─ img
└─ test-image.png
```

Output HTML folder:

```text
build_site
├─ featured-image.png
├─ img
│  └─ test-image.png
└─ index.html
```

Markdown file `test_01.md`:

```markdown
---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---

# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)
```

HTML file `index.html`:

```html
<h1 id="title">Title</h1>
<p><img src="featured-image.png" alt="Featured image" /></p>
<p>Hello, world!</p>
<p><img src="img/test-image.png" alt="Alt text" /></p>
```

# List of processed YAML variables

- `date`: Date of creation of the article.
- `update`: Date of the article update.
- `categories`: The list of categories to which the article belongs. Spaces in category
  names are not allowed.
- `tags`: The list of tags to which the article belongs. Spaces in tags names are
  not allowed.
- `published`: `false` if the article is in drafts and should not be published.
  If the tag is not in YAML, the default value is `true`.
- `latex`: `true` if $LaTeX$ is used in the article. Example: `$y = x^{2}$`.
  If the tag is not in YAML, the default value is `false`.
- `related-id`: The key for linking several articles into a series of articles.
  If this parameter is present, then at the bottom of the article there will be
  a list of all articles with the same parameter value.
- `demo`: The link to the demo page.
- `download`: The link to the download file.
- `author`: Name of the author of the article.
- `author-email`: Email of the author of the article.
- `permalink`: The URL address of the article on the website.
- `permalink-source`: The URL address of the markdown file on GitHub (for example).
- `license`: The license name of this article.
- `license-url`: The URL address of the license file.
- `attribution`: The link (or array of links) to the source of the material.
- `lang`: Language of the article.

Example:

```yaml
---
date: 2018-08-03
update: 2022-09-19
categories: [it, web]
tags: [CSS, CSS-Grids]
published: false
latex: true
related-id: html-lesson
demo: https://codepen.io/Harrix/pen/pZZZxg
download: https://github.com/Harrix/Russian-Nouns/releases
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
permalink: https://harrix.dev/ru/blog/2018/install-latex/
permalink-source: https://github.com/Harrix/harrix.dev-blog-2018/blob/main/install-latex/install-latex.md
license: CC BY 4.0
license-url: https://github.com/Harrix/harrix.dev/blob/main/LICENSE.md
attribution: https://en.wikipedia.org/wiki/Genetic_algorithm
lang: ru
---
```

<details>
<summary>Code:</summary>

````python
class Article:

    def __init__(self, md_filename: str | Path) -> None:
        """Get all info of the Markdown file with folders.
        Constructor `__init__` does not generate new files and folders.

        Args:

        - `md_filename` (str | Path): Full filename of the Markdown file.

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("C:/GitHub/harrix-pyssg/tests/data/test_01/test_01.md")
        ```

        """
        self._html_folder = None
        self._md_yaml_dict = {}
        self.load(md_filename)

    def add_image_captions(self) -> Article:
        """Add captions to images. The method ignores a featured image
        (for example, `![Featured image](featured-image.svg)`). The method does not
        save changes to the file. This should be done using the `save()` method.
        The method automatically numbers the images.

        Returns:

        - `Article`: Returns itself, that is, the article with calculated data.

        Example:

        ```python
        import harrixpyssg as hsg

        md_filename = "./tests/data/test_01/test_01.md"
        a = hsg.Article(md_filename)
        a.add_image_captions()
        print(a.md_content)
        ```

        Before:

        ```
        ---
        date: 2022-09-18
        categories: [it, web]
        tags: [CSS]
        ---

        # Title

        ![Featured image](featured-image.png)

        Hello, world!

        ![Alt text](img/test-image.png)
        ```

        After:

        ```
        ---
        date: 2022-09-18
        categories: [it, web]
        tags: [CSS]
        ---

        # Title

        ![Featured image](featured-image.png)

        Hello, world!

        ![Alt text](img/test-image.png)

        _Figure 1: Alt text_
        ```

        """
        index_images = 1
        content_parts = self._get_nocode_code_parts()
        for i in range(len(content_parts)):
            if content_parts[i][1]:
                continue
            lines = content_parts[i][0].split("\n")
            for j in range(len(lines)):
                if str(lines[j])[:2] not in ["![", "<i"]:
                    continue
                if str(lines[j]).startswith("![Featured image]("):
                    continue
                regexp = r"^\!\[(.*?)\]\((.*?)\)"
                regexp_html = r"^\<img alt=\"(.*?)\" src=\"(.*?)\" (.*?)\>"
                find = re.search(regexp, lines[j], re.DOTALL)
                if not find:
                    find = re.search(regexp_html, lines[j], re.DOTALL)
                if find:
                    if "lang" in self.md_yaml_dict and self.md_yaml_dict["lang"] == "ru":
                        caption = f"_Рисунок {index_images} — {find.group(1)}_"
                    else:
                        caption = f"_Figure {index_images}: {find.group(1)}_"
                    if j < len(lines) - 2 and (lines[j + 2].startswith("_Рис") or lines[j + 2].startswith("_Fig")):
                        lines[j + 2] = caption
                    else:
                        lines[j] += "\n\n" + caption
                    index_images += 1
            processed_part = "\n".join(lines)
            content_parts[i] = (processed_part, content_parts[i][1])
        processed_content = "\n".join([x[0] for x in content_parts])
        self._md_content_no_yaml = processed_content
        return self

    @property
    def featured_image_filenames(self) -> list[str]:
        """`list[str]`: Array of featured images. The files must be in the same folder
        as the Markdown file. Example: `["featured-image.png", "featured-image.svg"]`.

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        article.html_folder = "./build_site"
        print(article.featured_image_filenames)
        # ['featured-image.png']
        ```

        """
        res = []
        for file in self.md_filename.parent.iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                res.append(file.name)
        return res

    def generate_html(self, html_folder=None) -> Article:
        """Generate HTML file with folders from the Markdown file with folders.

        Args:

        - `html_folder` (str | Path): Output folder of the HTML file. Default: `None`.

        Returns:

        - `Article`: Returns itself, that is, the article with calculated data.

        Example:

        ```python
        import harrixpyssg as hsg

        md_filename = "./tests/data/test_01/test_01.md"
        html_folder = "./build_site"
        article = hsg.Article(md_filename)
        article.generate_html(html_folder)
        ```

        """
        if html_folder is not None:
            self.html_folder = html_folder

        self._clear_html_folder_directory()
        self._copy_dirs()
        self._copy_featured_images()

        if self.html_filename is not None:
            self.html_filename.write_text(self.html_code, encoding="utf8")
        return self

    @property
    def html_code(self) -> str:
        """`str`: HTML clean code from the Markdown code (only getter).

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        print(article.html_code())
        ```

        Example output:

        ```html
        <h1 id="title">Title</h1>
        <p><img src="featured-image.png" alt="Featured image" /></p>
        <p>Hello, world!</p>
        <p><img src="img/test-image.png" alt="Alt text" /></p>
        ```

        """
        md = (
            MarkdownIt("gfm-like", {"typographer": True, "linkify": False})
            .use(front_matter_plugin)
            .use(tasklists_plugin)
            .use(anchors_plugin)
            .use(dollarmath_plugin)
            .use(footnote_plugin)
            .enable(["replacements"])
        )

        return md.render(self.md_content).lstrip()

    @property
    def html_filename(self) -> Path | None:
        r"""`Path | None`: Output filename of HTML file (only getter).

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        article.html_folder = "./build_site"
        print(article.html_filename)
        # C:\\GitHub\\harrix-pyssg\build_site\\index.html
        ```
        """
        if self._html_folder is not None:
            return (self._html_folder / "index.html").absolute()
        return None

    @property
    def html_folder(self) -> Path | None:
        r"""`Path | None`: Output folder of HTML file.

        Example for the getter:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        article.generate_html("./build_site")
        print(article.html_folder)
        # C:\\GitHub\\harrix-pyssg\build_site
        ```

        Example for the setter:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        article.html_folder = "./build_site"
        article.generate_html()
        ```
        """
        if self._html_folder is not None:
            return self._html_folder.absolute()
        return None

    @html_folder.setter
    def html_folder(self, new_value: str | Path) -> None:
        self._html_folder = Path(new_value)

    def load(self, md_filename: str | Path) -> None:
        r"""Loads a new Markdown file.

        Args:

        - `md_filename` (str | Path): Full filename of the Markdown file.

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        article.load("./tests/data/test_02/test_02.md")
        print(article.md_filename)
        # tests\\data\test_02\test_02.md
        ```

        """
        self._md_filename = Path(md_filename)
        try:
            md = Path(self.md_filename).read_text(encoding="utf8").lstrip()

            self._md_content_no_yaml = re.sub(r"^---(.|\n)*?---\n", "", md).lstrip()

            find = re.search(r"^---(.|\n)*?---\n", md, re.DOTALL)
            if find:
                yaml_text = find.group().rstrip()[:-4].rstrip()
                self._md_yaml_dict = yaml.safe_load(yaml_text)
        except Exception:
            logger.error(f'The file "{md_filename}" does not open')

    @property
    def md_content(self) -> str:
        """`str`: The contents of the Markdown file (only getter). A block with YAML may
        differ from how it looks in the Markdown file.

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        print(article.md_content)
        ```

        Example output:

        ```markdown
        ---
        date: 2022-09-18
        categories: [it, web]
        tags: [CSS]
        ---

        # Title

        ![Featured image](featured-image.png)

        Hello, world!

        ![Alt text](img/test-image.png)
        ```

        """
        return f"{self.md_yaml}\n\n{self.md_content_no_yaml.rstrip()}\n".lstrip()

    @property
    def md_content_no_yaml(self) -> str:
        """`str`: Text of the article in the form of Markdown without YAML text.

        Example for the getter:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        print(article.md_content_no_yaml)
        ```

        Example output:

        ```md
        # Title

        ![Featured image](featured-image.png)

        Hello, world!

        ![Alt text](img/test-image.png)
        ```

        Example for the setter:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        article.md_content_no_yaml = "# New content"
        print(article.md_content_no_yaml)
        # # New content
        ```
        """
        return self._md_content_no_yaml

    @md_content_no_yaml.setter
    def md_content_no_yaml(self, new_value: str) -> None:
        self._md_content_no_yaml = new_value

    @property
    def md_filename(self) -> Path:
        r"""`Path`: Full filename of the Markdown file (only getter).
        Example: `"./tests/data/test_01/test_01.md"`.

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        print(article.md_filename)
        # C:\\GitHub\\harrix-pyssg\tests\\data\test_01\test_01.md
        ```

        You can upload a new file and change the value of this variable via
        method `load(path_new_md_file)`.
        """
        return self._md_filename.absolute()

    @property
    def md_yaml(self) -> str:
        """`str`: YAML from the Markdown file (only getter).

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        print(article.md_yaml)
        ```

        Example output:

        ```yaml
        ---
        date: 2022-09-18
        categories: [it, web]
        tags: [CSS]
        ---
        ```

        """
        if len(self.md_yaml_dict) == 0:
            return ""
        res = yaml.safe_dump(
            self._md_yaml_dict,
            sort_keys=False,
            allow_unicode=True,
            explicit_start=True,
            default_flow_style=None,
        )
        if res.startswith("--- {"):
            res = yaml.safe_dump(
                self._md_yaml_dict,
                sort_keys=False,
                allow_unicode=True,
                explicit_start=True,
                default_flow_style=False,
            )
        return res + "---"

    @property
    def md_yaml_dict(self) -> dict:
        r"""`dict`: YAML from the Markdown file (only getter, but you can change
        the contents of the dictionary).

        Example:

        ```python
        import datetime
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        print(*article.md_yaml_dict.items(), sep="\n")
        article.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
        print(article.md_yaml)
        ```

        Example output:

        ```shell
        ('date', datetime.date(2022, 9, 18))
        ('categories', ['it', 'web'])
        ('tags', ['CSS'])
        ---
        date: 2022-11-04
        categories: [it, web]
        tags: [CSS]
        ---
        ```

        """
        return self._md_yaml_dict

    def save(self) -> None:
        r"""Save the Markdown file.

        Example:

        ```python
        import harrixpyssg as hsg

        article = hsg.Article("./tests/data/test_01/test_01.md")
        a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
        a.md_content_no_yaml = "# New title\n\nNew content"
        a.save()
        ```

        """
        try:
            Path(self.md_filename).write_text(self.md_content, encoding="utf8")
        except Exception:
            logger.error(f'The file "{self.md_filename}" does not save')

    def to_sub_article(self) -> str:
        """Convert article to sub-article format by increasing heading levels."""

        def fix_part(no_code_part):
            """Replace `# Title` to `## Title`.
            Replace `![Alt text](img/test-image.png)`
            to `![Alt text](test_01/img/test-image.png)`.
            """
            lines = no_code_part.split("\n")
            for i in range(len(lines)):
                is_title = False
                for j in range(5):
                    # Replace headings.
                    hash_prefix = "#" * (j + 1) + " "
                    hash_replace = "#" * (j + 2) + " "
                    if not lines[i].startswith(hash_prefix):
                        continue
                    lines[i] = lines[i].replace(hash_prefix, hash_replace, 1)
                    is_title = True
                    break
                if not is_title:
                    # Replace headings.
                    regexp = r"(?:(?!`|`!))\[(.*?)\]\(((?!http).*?)\)"
                    pattern = re.compile(regexp)
                    lines[i] = re.sub(
                        pattern,
                        rf"[\1]({self.md_filename.parts[-2]}/\2)",
                        lines[i],
                    )

            return "\n".join(lines)

        return self._process_no_code_content(fix_part)

    def _clear_html_folder_directory(self) -> None:
        """This method clears `self.html_folder` with sub-directories."""
        if self.html_folder is None:
            return
        if self.html_folder.exists() and self.html_folder.is_dir():
            shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)

    def _copy_dirs(self) -> None:
        """This method copies all folders from the directory with the Markdown file."""
        if self.html_folder is None:
            return
        for file in Path(self.md_filename).parent.iterdir():
            if file.is_dir():
                shutil.copytree(file, self.html_folder / file.name, dirs_exist_ok=True)

    def _copy_featured_images(self) -> None:
        """This method copies all featured images from the directory with
        the Markdown file.
        """
        if self.html_folder is None:
            return
        for filename in self.featured_image_filenames:
            file = self.md_filename.parent / filename
            output_file = self.html_folder / filename
            shutil.copy(file, output_file)

    def _get_nocode_code_parts(self) -> list:
        r"""The method returns an array of tuples: part of the markdown file,
        True if part of the file is a piece of code.

        Example:

        File `test.md`:

        ```
        # Heading

        Text.

        ```python
        x = input()
        ```

        Text 2.

        ```

        ```python
        md_filename = "test.md"
        a = hsg.Article(md_filename)
        print(*a._get_nocode_code_parts(), sep="\n")
        # ('# Heading\n\nText.\n', False)
        # ('```python\nx = input()\n```', True)
        # ('\nText 2.', False)
        ```

        """
        res = []
        lines = self.md_content_no_yaml.splitlines()
        starts = ["`" * 6, "`" * 5, "`" * 4, "`" * 3]
        start_space = " " * 4
        part = []
        is_code = False
        start_code_now = None
        for i in range(len(lines)):
            for start_code in starts:
                if not is_code and lines[i].lstrip().startswith(start_code):
                    if part:
                        res.append(("\n".join(part), is_code))
                    part = [lines[i]]
                    is_code = True
                    start_code_now = start_code
                    break
                if lines[i].lstrip().startswith(start_code) and start_code_now == start_code:
                    part.append(lines[i])
                    if part:
                        res.append(("\n".join(part), is_code))
                    is_code = False
                    start_code_now = None
                    part = []
                    break
            else:
                if not is_code and lines[i].startswith(start_space):
                    if i == 0 or lines[i - 1] == "":
                        if part:
                            res.append(("\n".join(part), is_code))
                        part = [lines[i]]
                        is_code = True
                        start_code_now = start_space
                elif is_code and start_code_now == start_space and i < len(lines) - 1:
                    next_line = lines[i + 1].rstrip()
                    if len(next_line) > 0 and next_line[0] != " ":
                        part.append(lines[i])
                        if part:
                            res.append(("\n".join(part), is_code))
                        is_code = False
                        start_code_now = None
                        part = []
                    else:
                        part.append(lines[i])
                else:
                    part.append(lines[i])
        if part:
            res.append(("\n".join(part), is_code))
        return res

    def _process_no_code_content(self, func) -> str:
        r"""This method handles all parts of the markdown without the code
        using the function `func`.

        Example:

        ```python
        def fix_part(no_code_part):
            lines = no_code_part.split("\n")
            lines.append("Код:")
            return "\n".join(lines)

        self._md_content_no_yaml = self._process_no_code_content(fix_part)
        ```

        """
        content_parts = self._get_nocode_code_parts()
        for i in range(len(content_parts)):
            if content_parts[i][1]:
                continue
            processed_part = func(content_parts[i][0])
            content_parts[i] = (processed_part, content_parts[i][1])
        return "\n".join([x[0] for x in content_parts])
````

</details>

### ⚙️ Method `__init__`

```python
def __init__(self, md_filename: str | Path) -> None
```

Get all info of the Markdown file with folders.
Constructor `__init__` does not generate new files and folders.

Args:

- `md_filename` (str | Path): Full filename of the Markdown file.

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("C:/GitHub/harrix-pyssg/tests/data/test_01/test_01.md")
```

<details>
<summary>Code:</summary>

```python
def __init__(self, md_filename: str | Path) -> None:
        self._html_folder = None
        self._md_yaml_dict = {}
        self.load(md_filename)
```

</details>

### ⚙️ Method `add_image_captions`

```python
def add_image_captions(self) -> Article
```

Add captions to images. The method ignores a featured image
(for example, `![Featured image](featured-image.svg)`). The method does not
save changes to the file. This should be done using the `save()` method.
The method automatically numbers the images.

Returns:

- `Article`: Returns itself, that is, the article with calculated data.

Example:

```python
import harrixpyssg as hsg

md_filename = "./tests/data/test_01/test_01.md"
a = hsg.Article(md_filename)
a.add_image_captions()
print(a.md_content)
```

Before:

```
---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---

# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)
```

After:

```
---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---

# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)

_Figure 1: Alt text_
```

<details>
<summary>Code:</summary>

```python
def add_image_captions(self) -> Article:
        index_images = 1
        content_parts = self._get_nocode_code_parts()
        for i in range(len(content_parts)):
            if content_parts[i][1]:
                continue
            lines = content_parts[i][0].split("\n")
            for j in range(len(lines)):
                if str(lines[j])[:2] not in ["![", "<i"]:
                    continue
                if str(lines[j]).startswith("![Featured image]("):
                    continue
                regexp = r"^\!\[(.*?)\]\((.*?)\)"
                regexp_html = r"^\<img alt=\"(.*?)\" src=\"(.*?)\" (.*?)\>"
                find = re.search(regexp, lines[j], re.DOTALL)
                if not find:
                    find = re.search(regexp_html, lines[j], re.DOTALL)
                if find:
                    if "lang" in self.md_yaml_dict and self.md_yaml_dict["lang"] == "ru":
                        caption = f"_Рисунок {index_images} — {find.group(1)}_"
                    else:
                        caption = f"_Figure {index_images}: {find.group(1)}_"
                    if j < len(lines) - 2 and (lines[j + 2].startswith("_Рис") or lines[j + 2].startswith("_Fig")):
                        lines[j + 2] = caption
                    else:
                        lines[j] += "\n\n" + caption
                    index_images += 1
            processed_part = "\n".join(lines)
            content_parts[i] = (processed_part, content_parts[i][1])
        processed_content = "\n".join([x[0] for x in content_parts])
        self._md_content_no_yaml = processed_content
        return self
```

</details>

### ⚙️ Method `featured_image_filenames`

```python
def featured_image_filenames(self) -> list[str]
```

`list[str]`: Array of featured images. The files must be in the same folder
as the Markdown file. Example: `["featured-image.png", "featured-image.svg"]`.

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
article.html_folder = "./build_site"
print(article.featured_image_filenames)
# ['featured-image.png']
```

<details>
<summary>Code:</summary>

```python
def featured_image_filenames(self) -> list[str]:
        res = []
        for file in self.md_filename.parent.iterdir():
            if file.is_file() and file.name.startswith("featured-image"):
                res.append(file.name)
        return res
```

</details>

### ⚙️ Method `generate_html`

```python
def generate_html(self, html_folder = None) -> Article
```

Generate HTML file with folders from the Markdown file with folders.

Args:

- `html_folder` (str | Path): Output folder of the HTML file. Default: `None`.

Returns:

- `Article`: Returns itself, that is, the article with calculated data.

Example:

```python
import harrixpyssg as hsg

md_filename = "./tests/data/test_01/test_01.md"
html_folder = "./build_site"
article = hsg.Article(md_filename)
article.generate_html(html_folder)
```

<details>
<summary>Code:</summary>

```python
def generate_html(self, html_folder=None) -> Article:
        if html_folder is not None:
            self.html_folder = html_folder

        self._clear_html_folder_directory()
        self._copy_dirs()
        self._copy_featured_images()

        if self.html_filename is not None:
            self.html_filename.write_text(self.html_code, encoding="utf8")
        return self
```

</details>

### ⚙️ Method `html_code`

```python
def html_code(self) -> str
```

`str`: HTML clean code from the Markdown code (only getter).

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
print(article.html_code())
```

Example output:

```html
<h1 id="title">Title</h1>
<p><img src="featured-image.png" alt="Featured image" /></p>
<p>Hello, world!</p>
<p><img src="img/test-image.png" alt="Alt text" /></p>
```

<details>
<summary>Code:</summary>

```python
def html_code(self) -> str:
        md = (
            MarkdownIt("gfm-like", {"typographer": True, "linkify": False})
            .use(front_matter_plugin)
            .use(tasklists_plugin)
            .use(anchors_plugin)
            .use(dollarmath_plugin)
            .use(footnote_plugin)
            .enable(["replacements"])
        )

        return md.render(self.md_content).lstrip()
```

</details>

### ⚙️ Method `html_filename`

```python
def html_filename(self) -> Path | None
```

`Path | None`: Output filename of HTML file (only getter).

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
article.html_folder = "./build_site"
print(article.html_filename)
# C:\\GitHub\\harrix-pyssg\build_site\\index.html
```

<details>
<summary>Code:</summary>

```python
def html_filename(self) -> Path | None:
        if self._html_folder is not None:
            return (self._html_folder / "index.html").absolute()
        return None
```

</details>

### ⚙️ Method `html_folder`

```python
def html_folder(self) -> Path | None
```

`Path | None`: Output folder of HTML file.

Example for the getter:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
article.generate_html("./build_site")
print(article.html_folder)
# C:\\GitHub\\harrix-pyssg\build_site
```

Example for the setter:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
article.html_folder = "./build_site"
article.generate_html()
```

<details>
<summary>Code:</summary>

```python
def html_folder(self) -> Path | None:
        if self._html_folder is not None:
            return self._html_folder.absolute()
        return None
```

</details>

### ⚙️ Method `html_folder`

```python
def html_folder(self, new_value: str | Path) -> None
```

_No docstring provided._

<details>
<summary>Code:</summary>

```python
def html_folder(self, new_value: str | Path) -> None:
        self._html_folder = Path(new_value)
```

</details>

### ⚙️ Method `load`

```python
def load(self, md_filename: str | Path) -> None
```

Loads a new Markdown file.

Args:

- `md_filename` (str | Path): Full filename of the Markdown file.

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
article.load("./tests/data/test_02/test_02.md")
print(article.md_filename)
# tests\\data\test_02\test_02.md
```

<details>
<summary>Code:</summary>

```python
def load(self, md_filename: str | Path) -> None:
        self._md_filename = Path(md_filename)
        try:
            md = Path(self.md_filename).read_text(encoding="utf8").lstrip()

            self._md_content_no_yaml = re.sub(r"^---(.|\n)*?---\n", "", md).lstrip()

            find = re.search(r"^---(.|\n)*?---\n", md, re.DOTALL)
            if find:
                yaml_text = find.group().rstrip()[:-4].rstrip()
                self._md_yaml_dict = yaml.safe_load(yaml_text)
        except Exception:
            logger.error(f'The file "{md_filename}" does not open')
```

</details>

### ⚙️ Method `md_content`

```python
def md_content(self) -> str
```

`str`: The contents of the Markdown file (only getter). A block with YAML may
differ from how it looks in the Markdown file.

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
print(article.md_content)
```

Example output:

```markdown
---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---

# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)
```

<details>
<summary>Code:</summary>

```python
def md_content(self) -> str:
        return f"{self.md_yaml}\n\n{self.md_content_no_yaml.rstrip()}\n".lstrip()
```

</details>

### ⚙️ Method `md_content_no_yaml`

```python
def md_content_no_yaml(self) -> str
```

`str`: Text of the article in the form of Markdown without YAML text.

Example for the getter:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
print(article.md_content_no_yaml)
```

Example output:

```md
# Title

![Featured image](featured-image.png)

Hello, world!

![Alt text](img/test-image.png)
```

Example for the setter:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
article.md_content_no_yaml = "# New content"
print(article.md_content_no_yaml)
# # New content
```

<details>
<summary>Code:</summary>

```python
def md_content_no_yaml(self) -> str:
        return self._md_content_no_yaml
```

</details>

### ⚙️ Method `md_content_no_yaml`

```python
def md_content_no_yaml(self, new_value: str) -> None
```

_No docstring provided._

<details>
<summary>Code:</summary>

```python
def md_content_no_yaml(self, new_value: str) -> None:
        self._md_content_no_yaml = new_value
```

</details>

### ⚙️ Method `md_filename`

```python
def md_filename(self) -> Path
```

`Path`: Full filename of the Markdown file (only getter).
Example: `"./tests/data/test_01/test_01.md"`.

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
print(article.md_filename)
# C:\\GitHub\\harrix-pyssg\tests\\data\test_01\test_01.md
```

You can upload a new file and change the value of this variable via
method `load(path_new_md_file)`.

<details>
<summary>Code:</summary>

```python
def md_filename(self) -> Path:
        return self._md_filename.absolute()
```

</details>

### ⚙️ Method `md_yaml`

```python
def md_yaml(self) -> str
```

`str`: YAML from the Markdown file (only getter).

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
print(article.md_yaml)
```

Example output:

```yaml
---
date: 2022-09-18
categories: [it, web]
tags: [CSS]
---
```

<details>
<summary>Code:</summary>

```python
def md_yaml(self) -> str:
        if len(self.md_yaml_dict) == 0:
            return ""
        res = yaml.safe_dump(
            self._md_yaml_dict,
            sort_keys=False,
            allow_unicode=True,
            explicit_start=True,
            default_flow_style=None,
        )
        if res.startswith("--- {"):
            res = yaml.safe_dump(
                self._md_yaml_dict,
                sort_keys=False,
                allow_unicode=True,
                explicit_start=True,
                default_flow_style=False,
            )
        return res + "---"
```

</details>

### ⚙️ Method `md_yaml_dict`

```python
def md_yaml_dict(self) -> dict
```

`dict`: YAML from the Markdown file (only getter, but you can change
the contents of the dictionary).

Example:

```python
import datetime
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
print(*article.md_yaml_dict.items(), sep="\n")
article.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
print(article.md_yaml)
```

Example output:

```shell
('date', datetime.date(2022, 9, 18))
('categories', ['it', 'web'])
('tags', ['CSS'])
---
date: 2022-11-04
categories: [it, web]
tags: [CSS]
---
```

<details>
<summary>Code:</summary>

```python
def md_yaml_dict(self) -> dict:
        return self._md_yaml_dict
```

</details>

### ⚙️ Method `save`

```python
def save(self) -> None
```

Save the Markdown file.

Example:

```python
import harrixpyssg as hsg

article = hsg.Article("./tests/data/test_01/test_01.md")
a.md_yaml_dict["date"] = datetime.date(2022, 11, 4)
a.md_content_no_yaml = "# New title\n\nNew content"
a.save()
```

<details>
<summary>Code:</summary>

```python
def save(self) -> None:
        try:
            Path(self.md_filename).write_text(self.md_content, encoding="utf8")
        except Exception:
            logger.error(f'The file "{self.md_filename}" does not save')
```

</details>

### ⚙️ Method `to_sub_article`

```python
def to_sub_article(self) -> str
```

Convert article to sub-article format by increasing heading levels.

<details>
<summary>Code:</summary>

```python
def to_sub_article(self) -> str:

        def fix_part(no_code_part):
            """Replace `# Title` to `## Title`.
            Replace `![Alt text](img/test-image.png)`
            to `![Alt text](test_01/img/test-image.png)`.
            """
            lines = no_code_part.split("\n")
            for i in range(len(lines)):
                is_title = False
                for j in range(5):
                    # Replace headings.
                    hash_prefix = "#" * (j + 1) + " "
                    hash_replace = "#" * (j + 2) + " "
                    if not lines[i].startswith(hash_prefix):
                        continue
                    lines[i] = lines[i].replace(hash_prefix, hash_replace, 1)
                    is_title = True
                    break
                if not is_title:
                    # Replace headings.
                    regexp = r"(?:(?!`|`!))\[(.*?)\]\(((?!http).*?)\)"
                    pattern = re.compile(regexp)
                    lines[i] = re.sub(
                        pattern,
                        rf"[\1]({self.md_filename.parts[-2]}/\2)",
                        lines[i],
                    )

            return "\n".join(lines)

        return self._process_no_code_content(fix_part)
```

</details>

### ⚙️ Method `_clear_html_folder_directory`

```python
def _clear_html_folder_directory(self) -> None
```

This method clears `self.html_folder` with sub-directories.

<details>
<summary>Code:</summary>

```python
def _clear_html_folder_directory(self) -> None:
        if self.html_folder is None:
            return
        if self.html_folder.exists() and self.html_folder.is_dir():
            shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)
```

</details>

### ⚙️ Method `_copy_dirs`

```python
def _copy_dirs(self) -> None
```

This method copies all folders from the directory with the Markdown file.

<details>
<summary>Code:</summary>

```python
def _copy_dirs(self) -> None:
        if self.html_folder is None:
            return
        for file in Path(self.md_filename).parent.iterdir():
            if file.is_dir():
                shutil.copytree(file, self.html_folder / file.name, dirs_exist_ok=True)
```

</details>

### ⚙️ Method `_copy_featured_images`

```python
def _copy_featured_images(self) -> None
```

This method copies all featured images from the directory with
the Markdown file.

<details>
<summary>Code:</summary>

```python
def _copy_featured_images(self) -> None:
        if self.html_folder is None:
            return
        for filename in self.featured_image_filenames:
            file = self.md_filename.parent / filename
            output_file = self.html_folder / filename
            shutil.copy(file, output_file)
```

</details>

### ⚙️ Method `_get_nocode_code_parts`

```python
def _get_nocode_code_parts(self) -> list
```

The method returns an array of tuples: part of the markdown file,
True if part of the file is a piece of code.

Example:

File `test.md`:

````
# Heading

Text.

```python
x = input()
````

Text 2.

````

```python
md_filename = "test.md"
a = hsg.Article(md_filename)
print(*a._get_nocode_code_parts(), sep="\n")
# ('# Heading\n\nText.\n', False)
# ('```python\nx = input()\n```', True)
# ('\nText 2.', False)
````

<details>
<summary>Code:</summary>

```python
def _get_nocode_code_parts(self) -> list:
        res = []
        lines = self.md_content_no_yaml.splitlines()
        starts = ["`" * 6, "`" * 5, "`" * 4, "`" * 3]
        start_space = " " * 4
        part = []
        is_code = False
        start_code_now = None
        for i in range(len(lines)):
            for start_code in starts:
                if not is_code and lines[i].lstrip().startswith(start_code):
                    if part:
                        res.append(("\n".join(part), is_code))
                    part = [lines[i]]
                    is_code = True
                    start_code_now = start_code
                    break
                if lines[i].lstrip().startswith(start_code) and start_code_now == start_code:
                    part.append(lines[i])
                    if part:
                        res.append(("\n".join(part), is_code))
                    is_code = False
                    start_code_now = None
                    part = []
                    break
            else:
                if not is_code and lines[i].startswith(start_space):
                    if i == 0 or lines[i - 1] == "":
                        if part:
                            res.append(("\n".join(part), is_code))
                        part = [lines[i]]
                        is_code = True
                        start_code_now = start_space
                elif is_code and start_code_now == start_space and i < len(lines) - 1:
                    next_line = lines[i + 1].rstrip()
                    if len(next_line) > 0 and next_line[0] != " ":
                        part.append(lines[i])
                        if part:
                            res.append(("\n".join(part), is_code))
                        is_code = False
                        start_code_now = None
                        part = []
                    else:
                        part.append(lines[i])
                else:
                    part.append(lines[i])
        if part:
            res.append(("\n".join(part), is_code))
        return res
```

</details>

### ⚙️ Method `_process_no_code_content`

```python
def _process_no_code_content(self, func) -> str
```

This method handles all parts of the markdown without the code
using the function `func`.

Example:

```python
def fix_part(no_code_part):
    lines = no_code_part.split("\n")
    lines.append("Код:")
    return "\n".join(lines)

self._md_content_no_yaml = self._process_no_code_content(fix_part)
```

<details>
<summary>Code:</summary>

```python
def _process_no_code_content(self, func) -> str:
        content_parts = self._get_nocode_code_parts()
        for i in range(len(content_parts)):
            if content_parts[i][1]:
                continue
            processed_part = func(content_parts[i][0])
            content_parts[i] = (processed_part, content_parts[i][1])
        return "\n".join([x[0] for x in content_parts])
```

</details>

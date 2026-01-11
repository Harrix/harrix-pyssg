---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# 📄 File `static_site_generator.py`

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🏛️ Class `StaticSiteGenerator`](#%EF%B8%8F-class-staticsitegenerator)
- [Usage examples](#usage-examples)
- [Example of folder structure](#example-of-folder-structure)
  - [⚙️ Method `__init__`](#%EF%B8%8F-method-__init__)
  - [⚙️ Method `add_image_captions`](#%EF%B8%8F-method-add_image_captions)
  - [⚙️ Method `add_yaml_tag_to_all_md`](#%EF%B8%8F-method-add_yaml_tag_to_all_md)
  - [⚙️ Method `articles`](#%EF%B8%8F-method-articles)
  - [⚙️ Method `generate_generalized_md`](#%EF%B8%8F-method-generate_generalized_md)
  - [⚙️ Method `generate_site`](#%EF%B8%8F-method-generate_site)
  - [⚙️ Method `get_set_variables_from_yaml`](#%EF%B8%8F-method-get_set_variables_from_yaml)
  - [⚙️ Method `html_folder`](#%EF%B8%8F-method-html_folder)
  - [⚙️ Method `html_folder`](#%EF%B8%8F-method-html_folder-1)
  - [⚙️ Method `md_folder`](#%EF%B8%8F-method-md_folder)
  - [⚙️ Method `_clear_html_folder_directory`](#%EF%B8%8F-method-_clear_html_folder_directory)
  - [⚙️ Method `_get_info_about_articles`](#%EF%B8%8F-method-_get_info_about_articles)

</details>

## 🏛️ Class `StaticSiteGenerator`

```python
class StaticSiteGenerator
```

Static site generator. It collects Markdown files from folder and sub-folders.

## Usage examples

```python
import harrix_pyssg as hsg

md_folder = "C:/GitHub/harrix.dev/content"
html_folder = "C:/GitHub/harrix.dev/build_site"
sg = hsg.StaticSiteGenerator(md_folder)
sg.generate_site(html_folder)
```

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
html_folder = "./build_site"
sg = hsg.StaticSiteGenerator(md_folder)
sg.generate_site(html_folder)
```

## Example of folder structure

Folder with the Markdown files:

```text
data
├─ test_01
│  ├─ featured-image.png
│  ├─ img
│  │  └─ test-image.png
│  └─ test_01.md
└─ test_02
├─ featured-image.png
├─ img
│  └─ test-image.png
└─ test_02.md
```

Output HTML folder:

```text
build_site
├─ test_01
│  ├─ featured-image.png
│  ├─ img
│  │  └─ test-image.png
│  └─ index.html
└─ test_02
├─ featured-image.png
├─ img
│  └─ test-image.png
└─ index.html
```

<details>
<summary>Code:</summary>

````python
class StaticSiteGenerator:

    def __init__(self, md_folder: str | Path) -> None:
        """The generator collects Markdown files from folder and sub-folders.
        Constructor `__init__` does not generate new files and folders.

        Attributes:

        - `md_folder` (str | Path): Folder with Markdown files.
          Example: `"./tests/data"`.

        Example:

        ```python
        import harrix_pyssg as hsg

        sg = hsg.StaticSiteGenerator("C:/GitHub/harrix.dev/content")
        ```

        """
        self._md_folder = Path(md_folder)
        self._articles: list[Article] = []
        self._html_folder = None

        self._get_info_about_articles()

    def add_image_captions(self) -> StaticSiteGenerator:
        """Add captions to all images in all markdown files. The method ignores
        a featured image (for example, `![Featured image](featured-image.svg)`).
        The method saves changes to the file. The method automatically numbers
        the images.

        Returns:

        - `Article`: Returns itself.

        Example:

        ```python
        import harrix_pyssg as hsg

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
        for article in self.articles:
            article.add_image_captions()
            article.save()
        return self

    def add_yaml_tag_to_all_md(self, tuple_yaml_tag) -> None:
        """This method adds a YAML tag to all markdown files and save them.

        Args:

        - `tuple_yaml_tag`: Tuple of YAML tag. Example: `("author", "Anton Sergienko")`

        Returns:

        - `None`.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.add_yaml_tag_to_all_md(("author", "Anton Sergienko"))
        ```

        """
        if not isinstance(tuple_yaml_tag, tuple) and len(tuple_yaml_tag) != 2:
            return

        for article in self.articles:
            article.md_yaml_dict[tuple_yaml_tag[0]] = tuple_yaml_tag[1]
            article.save()

    @property
    def articles(self):
        r"""`list[Article]`: list of all articles that is generated in the `__init__()`.

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        articles = sg.articles # list of all articles
        print(sg.articles[0].md_filename)
        # C:\\GitHub\\harrix-pyssg\tests\\data\test_01\test_01.md
        ```
        """
        return self._articles

    def generate_generalized_md(self) -> None:
        """Generate generalized markdown files from articles in folders."""
        paths_generalized_md = set()
        # Get a list of paths that have MD files (without `.auto.md`)
        for article in self.articles:
            if ".auto.md" not in article.md_filename.name.lower():
                paths_generalized_md.add(article.md_filename.parent.parent)
        for path in paths_generalized_md:
            content_of_articles = []
            # Collect all articles from one folder
            for article in self.articles:
                if article.md_filename.parent.parent != path:
                    continue
                content = article.to_sub_article().strip()

                content_of_articles.append(content)
            # Save a new article in a directory level higher
            if content_of_articles:
                folder = path.parts[-1]
                title = f"# {folder} (auto-generated)\n\n"
                content = title + "\n\n".join(content_of_articles) + "\n"
                Path(path / f"{folder}.auto.md").write_text(content, encoding="utf8")

    def generate_site(self, html_folder=None) -> StaticSiteGenerator:
        """This method generates HTML files with folders from Markdown files.

        Args:

        - `html_folder` (str | Path): Output folder of the HTML files. Default: `None`.

        Returns:

        - `StaticSiteGenerator`: Returns itself.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        html_folder = "./build_site"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(html_folder)
        ```

        """
        if html_folder is not None:
            self.html_folder = html_folder
        if self.html_folder is None:
            return self

        self._clear_html_folder_directory()

        for article in self.articles:
            parts = list(article.md_filename.parts[len(self.md_folder.parts) : -1])
            html_folder_article = self.html_folder / "/".join(parts)
            html_folder_article.mkdir(parents=True, exist_ok=True)
            article.generate_html(html_folder_article)

        return self

    def get_set_variables_from_yaml(self):
        """This method generates a set of all variables from YAML from all articles.

        Returns:

        - `set[str]`: Sorted set of all variables from YAML from all articles.
          Example: `['categories', 'date', 'tags']`.

        Example:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        print(sg.get_set_variables_from_yaml())
        # ['categories', 'date', 'tags']
        ```

        """
        res = set()
        for article in self.articles:
            for key in article.md_yaml_dict:
                res.add(key)
        return sorted(res)

    @property
    def html_folder(self) -> Path | None:
        r"""`Path | None`: Output folder of HTML files.

        Example for the getter:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        html_folder = "./build_site"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.generate_site(html_folder)
        print(sg.html_folder)
        # C:\\GitHub\\harrix-pyssg\build_site
        ```

        Example for the setter:

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        sg.html_folder = "./build_site"
        sg.generate_site()
        ```
        """
        if self._html_folder is not None:
            return self._html_folder.absolute()
        return None

    @html_folder.setter
    def html_folder(self, new_value: str | Path) -> None:
        self._html_folder = Path(new_value)

    @property
    def md_folder(self):
        r"""`Path`: Folder with Markdown files (only getter).

        ```python
        import harrix_pyssg as hsg

        md_folder = "./tests/data"
        sg = hsg.StaticSiteGenerator(md_folder)
        print(sg.md_folder)
        # C:\\GitHub\\harrix-pyssg\tests\\data
        ```
        """
        return self._md_folder.absolute()

    def _clear_html_folder_directory(self) -> None:
        """This method clears `self.html_folder` with sub-directories."""
        if self.html_folder is None:
            return
        if self.html_folder.exists() and self.html_folder.is_dir():
            shutil.rmtree(self.html_folder)
        self.html_folder.mkdir(parents=True, exist_ok=True)

    def _get_info_about_articles(self) -> None:
        """This method gets info from all Markdown files and fills
        the list `self.articles`.
        """
        for item in filter(
            lambda path: not any(part for part in path.parts if part.startswith(".")),
            Path(self.md_folder).rglob("*"),
        ):
            if item.is_file() and item.suffix.lower() == ".md":
                self.articles.append(Article(item))
````

</details>

### ⚙️ Method `__init__`

```python
def __init__(self, md_folder: str | Path) -> None
```

The generator collects Markdown files from folder and sub-folders.
Constructor `__init__` does not generate new files and folders.

Attributes:

- `md_folder` (str | Path): Folder with Markdown files.
  Example: `"./tests/data"`.

Example:

```python
import harrix_pyssg as hsg

sg = hsg.StaticSiteGenerator("C:/GitHub/harrix.dev/content")
```

<details>
<summary>Code:</summary>

```python
def __init__(self, md_folder: str | Path) -> None:
        self._md_folder = Path(md_folder)
        self._articles: list[Article] = []
        self._html_folder = None

        self._get_info_about_articles()
```

</details>

### ⚙️ Method `add_image_captions`

```python
def add_image_captions(self) -> StaticSiteGenerator
```

Add captions to all images in all markdown files. The method ignores
a featured image (for example, `![Featured image](featured-image.svg)`).
The method saves changes to the file. The method automatically numbers
the images.

Returns:

- `Article`: Returns itself.

Example:

```python
import harrix_pyssg as hsg

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
def add_image_captions(self) -> StaticSiteGenerator:
        for article in self.articles:
            article.add_image_captions()
            article.save()
        return self
```

</details>

### ⚙️ Method `add_yaml_tag_to_all_md`

```python
def add_yaml_tag_to_all_md(self, tuple_yaml_tag) -> None
```

This method adds a YAML tag to all markdown files and save them.

Args:

- `tuple_yaml_tag`: Tuple of YAML tag. Example: `("author", "Anton Sergienko")`

Returns:

- `None`.

Example:

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
sg = hsg.StaticSiteGenerator(md_folder)
sg.add_yaml_tag_to_all_md(("author", "Anton Sergienko"))
```

<details>
<summary>Code:</summary>

```python
def add_yaml_tag_to_all_md(self, tuple_yaml_tag) -> None:
        if not isinstance(tuple_yaml_tag, tuple) and len(tuple_yaml_tag) != 2:
            return

        for article in self.articles:
            article.md_yaml_dict[tuple_yaml_tag[0]] = tuple_yaml_tag[1]
            article.save()
```

</details>

### ⚙️ Method `articles`

```python
def articles(self)
```

`list[Article]`: list of all articles that is generated in the `__init__()`.

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
sg = hsg.StaticSiteGenerator(md_folder)
articles = sg.articles # list of all articles
print(sg.articles[0].md_filename)
# C:\\GitHub\\harrix-pyssg\tests\\data\test_01\test_01.md
```

<details>
<summary>Code:</summary>

```python
def articles(self):
        return self._articles
```

</details>

### ⚙️ Method `generate_generalized_md`

```python
def generate_generalized_md(self) -> None
```

Generate generalized markdown files from articles in folders.

<details>
<summary>Code:</summary>

```python
def generate_generalized_md(self) -> None:
        paths_generalized_md = set()
        # Get a list of paths that have MD files (without `.auto.md`)
        for article in self.articles:
            if ".auto.md" not in article.md_filename.name.lower():
                paths_generalized_md.add(article.md_filename.parent.parent)
        for path in paths_generalized_md:
            content_of_articles = []
            # Collect all articles from one folder
            for article in self.articles:
                if article.md_filename.parent.parent != path:
                    continue
                content = article.to_sub_article().strip()

                content_of_articles.append(content)
            # Save a new article in a directory level higher
            if content_of_articles:
                folder = path.parts[-1]
                title = f"# {folder} (auto-generated)\n\n"
                content = title + "\n\n".join(content_of_articles) + "\n"
                Path(path / f"{folder}.auto.md").write_text(content, encoding="utf8")
```

</details>

### ⚙️ Method `generate_site`

```python
def generate_site(self, html_folder = None) -> StaticSiteGenerator
```

This method generates HTML files with folders from Markdown files.

Args:

- `html_folder` (str | Path): Output folder of the HTML files. Default: `None`.

Returns:

- `StaticSiteGenerator`: Returns itself.

Example:

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
html_folder = "./build_site"
sg = hsg.StaticSiteGenerator(md_folder)
sg.generate_site(html_folder)
```

<details>
<summary>Code:</summary>

```python
def generate_site(self, html_folder=None) -> StaticSiteGenerator:
        if html_folder is not None:
            self.html_folder = html_folder
        if self.html_folder is None:
            return self

        self._clear_html_folder_directory()

        for article in self.articles:
            parts = list(article.md_filename.parts[len(self.md_folder.parts) : -1])
            html_folder_article = self.html_folder / "/".join(parts)
            html_folder_article.mkdir(parents=True, exist_ok=True)
            article.generate_html(html_folder_article)

        return self
```

</details>

### ⚙️ Method `get_set_variables_from_yaml`

```python
def get_set_variables_from_yaml(self)
```

This method generates a set of all variables from YAML from all articles.

Returns:

- `set[str]`: Sorted set of all variables from YAML from all articles.
  Example: `['categories', 'date', 'tags']`.

Example:

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
sg = hsg.StaticSiteGenerator(md_folder)
print(sg.get_set_variables_from_yaml())
# ['categories', 'date', 'tags']
```

<details>
<summary>Code:</summary>

```python
def get_set_variables_from_yaml(self):
        res = set()
        for article in self.articles:
            for key in article.md_yaml_dict:
                res.add(key)
        return sorted(res)
```

</details>

### ⚙️ Method `html_folder`

```python
def html_folder(self) -> Path | None
```

`Path | None`: Output folder of HTML files.

Example for the getter:

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
html_folder = "./build_site"
sg = hsg.StaticSiteGenerator(md_folder)
sg.generate_site(html_folder)
print(sg.html_folder)
# C:\\GitHub\\harrix-pyssg\build_site
```

Example for the setter:

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
sg = hsg.StaticSiteGenerator(md_folder)
sg.html_folder = "./build_site"
sg.generate_site()
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

### ⚙️ Method `md_folder`

```python
def md_folder(self)
```

`Path`: Folder with Markdown files (only getter).

```python
import harrix_pyssg as hsg

md_folder = "./tests/data"
sg = hsg.StaticSiteGenerator(md_folder)
print(sg.md_folder)
# C:\\GitHub\\harrix-pyssg\tests\\data
```

<details>
<summary>Code:</summary>

```python
def md_folder(self):
        return self._md_folder.absolute()
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

### ⚙️ Method `_get_info_about_articles`

```python
def _get_info_about_articles(self) -> None
```

This method gets info from all Markdown files and fills
the list `self.articles`.

<details>
<summary>Code:</summary>

```python
def _get_info_about_articles(self) -> None:
        for item in filter(
            lambda path: not any(part for part in path.parts if part.startswith(".")),
            Path(self.md_folder).rglob("*"),
        ):
            if item.is_file() and item.suffix.lower() == ".md":
                self.articles.append(Article(item))
```

</details>

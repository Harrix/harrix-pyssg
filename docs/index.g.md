---
author: Anton Sergienko
author-email: anton.b.sergienko@gmail.com
lang: en
---

# Harrix PySSG

![Featured image](https://raw.githubusercontent.com/Harrix/harrix-pyssg/refs/heads/main/img/featured-image.svg)

🔌 Simple static site generator in Python. **In development**.

<details>
<summary>📖 Contents ⬇️</summary>

## Contents

- [🛠️ Technologies](#%EF%B8%8F-technologies)
- [📦 Installation](#-installation)
- [📚 List of functions](#-list-of-functions)
  - [📄 File `article.py`](#-file-articlepy)
  - [📄 File `static_site_generator.py`](#-file-static_site_generatorpy)
- [📄 License](#-license)
- [👤 Author](#-author)

</details>

![GitHub](https://img.shields.io/badge/GitHub-harrix--pyssg-blue?logo=github) ![GitHub](https://img.shields.io/github/license/Harrix/harrix-pyssg) ![PyPI](https://img.shields.io/pypi/v/harrix-pyssg)

GitHub: <https://github.com/Harrix/harrix-pyssg>

Documentation: [docs](https://github.com/Harrix/harrix-pyssg/blob/main/docs/index.g.md)

## 🛠️ Technologies

Markdown processor: [markdown-it-py](https://pypi.org/project/markdown-it-py) <https://pypistats.org/packages/markdown-it-py>.

## 📦 Installation

Using `pip`:

```shell
pip install harrix-pyssg
```

Using `uv` (recommended):

```shell
uv add harrix-pyssg
```

## 📚 List of functions

### 📄 File `article.py`

Doc: [article.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/article.g.md)

| Function/Class                                                                                                   | Description                                      |
| ---------------------------------------------------------------------------------------------------------------- | ------------------------------------------------ |
| 🏛️ Class [`Article`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/article.g.md#%EF%B8%8F-class-article) | All information about one article from the site. |

### 📄 File `static_site_generator.py`

Doc: [static_site_generator.g.md](https://github.com/Harrix/harrix-pyssg/blob/main/docs/static_site_generator.g.md)

| Function/Class                                                                                                                                         | Description                                                                    |
| ------------------------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------------------------------ |
| 🏛️ Class [`StaticSiteGenerator`](https://github.com/Harrix/harrix-pyssg/blob/main/docs/static_site_generator.g.md#%EF%B8%8F-class-staticsitegenerator) | Static site generator. It collects Markdown files from folder and sub-folders. |

## 📄 License

This project is licensed under the [MIT License](https://github.com/Harrix/harrix-pyssg/blob/main/LICENSE.md).

## 👤 Author

Author: [Anton Sergienko](https://github.com/Harrix).

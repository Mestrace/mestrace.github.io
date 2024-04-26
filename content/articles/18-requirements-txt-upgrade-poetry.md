Title: 从requirements.txt升级到Poetry
Slug: requirements-txt-upgrade-poetry
Category: Computer Science
Date: 2024-03-23 14:00
Tags: Python
Summary: 将包管理方式从requirements.txt升级到Poetry

在Python软件开发中，笔者通常使用 `requirements.txt` 文件来管理项目的依赖。这个习惯源自于 `pip freeze` 命令，它能够简单地列出当前 Python 环境下的所有包及其版本号。无论项目规模大小，这都是一种简单而有效的方法，能够确保所有开发人员以及部署环境中运行的包版本保持一致。在 `requirements.txt` 中，开发者可以轻松地为每个包定义一个版本号，例如 `abc-def >= 0.8.3`。然而，在今天，随着Python使用者越来越多，项目也越来越庞大的情况下，这个早在08年就开始使用的包管理方法显得愈发过时（[pypa/pip@368a064](https://github.com/pypa/pip/commit/368a064ae4ca77ac540ef4aea3bf61dd3c2bccb1)）。

在手动管理依赖的情况下，开发者往往无法穷尽所有的依赖关系。因此，通常的做法是只列出顶层依赖包及其版本号。这样一来，当依赖关系变得复杂时，pip 工具的解析能力就显得不足，无法自动解决依赖传递的问题。一个常见的情况是，不同的顶层包可能指定了同一个底层包的不同版本，并且这些版本可能相互不兼容。此外，当项目的依赖关系发生变化时，就需要大量手动操作来编辑 `requirements.txt` 文件。另外，不同的环境可能需要不同的依赖。作者通常会使用类似 `requirements-*.txt` 的命名方式来区分不同环境下的依赖。例如，在测试环境中，可能需要安装额外的跟踪相关库或测试库，如 `pytest`。但是，`requirements.txt` 无法完全锁定包的版本，因此在不同的环境中可能会安装不同的版本，甚至在极端情况下会引入安全风险。如果连接的不是受信任的仓库源，黑客可能会利用供应链攻击，将包版本替换为恶意软件版本，而`requirements.txt`无法解决这种问题。

在诸多选项中，笔者最终选择了`poetry`作为本博客的包管理工具。除了使用基于[PEP-621](https://peps.python.org/pep-0621/)带来的`pyproject.toml`的项目与包管理办法之外，`poetry`还带来了包版本锁定`poetry.lock`，增强的自动依赖解析器，配置工具，自动虚拟环境管理等多项功能。而接下来的内容则是一些简单的`poetry`命令介绍。

## poetry new

使用`poetry new`命令新建项目较为简单，在命令行里键入`poetry new <package-name>`即可。工具就新建对应名称的项目文件夹，并在其中包含`README.md`，`pyproject.toml`，源代码主目录及测试目录。但由于笔者是在现有环境中进行迁移，因此这个方式不太适用。

```text
> poetry new poetry-test
Created package poetry_test in poetry-test
> cd poetry-test 
> ls
README.md      poetry_test    pyproject.toml tests
```

而生成的`pyproject.toml`长这样。

```toml
[tool.poetry]
name = "poetry-test"
version = "0.1.0"
description = ""
authors = ["Mestrace <abc@example.com>"]
readme = "README.md"

[tool.poetry.dependencies]
python = "^3.11"

[build-system]
requires = ["poetry-core"]
build-backend = "poetry.core.masonry.api"
```

## poetry init

`poetry init`命令只在一个已有的项目下创建对应的`pyproject.toml`。使用`poetry init`之后，会进入一个命令行交互的引导，并输入对应的信息来填充生成的`pyproject.toml`，也是笔者迁移的第一步。

```text
> poetry init

This command will guide you through creating your pyproject.toml config.

Package name [mestrace.github.io]:  
Version [0.1.0]:  
Description []:  Mestrace's Personal Blog
Author [Mestrace <abc@example.com>, n to skip]:  n
License []:  WTFPL     
Compatible Python versions [^3.11]:  

Would you like to define your main dependencies interactively? (yes/no) [yes] no
Would you like to define your development dependencies interactively? (yes/no) [yes] no
```


## poetry add

`poetry add`则可以添加对应的包到当前项目，并解析对应的依赖

```text
> poetry add django@latest
Creating virtualenv poetry-test-Ewpj0lEl-py3.11 in /tmp/folder/virtualenvs
Using version ^5.0.3 for django

Updating dependencies
Resolving dependencies... (1.0s)

Package operations: 3 installs, 0 updates, 0 removals

  - Installing asgiref (3.8.1)
  - Installing sqlparse (0.4.4)
  - Installing django (5.0.3)

Writing lock file
```

添加之后，在`pyproject.toml`中新增了django的依赖。
```
[tool.poetry.dependencies]
python = "^3.11"
django = "^5.0.3"
```

此时，`poetry.lock`中也添加了对应的项目。要注意的是，这里也包含了对应`.whl`和`.tar.gz`文件的`sha256`的哈希校验码，以确保最终拉到的包是符合预期的。

```text
....

[[package]]
name = "django"
version = "5.0.3"
description = "A high-level Python web framework that encourages rapid development and clean, pragmatic design."
optional = false
python-versions = ">=3.10"
files = [
    {file = "Django-5.0.3-py3-none-any.whl", hash = "sha256:5c7d748ad113a81b2d44750ccc41edc14e933f56581683db548c9257e078cc83"},
    {file = "Django-5.0.3.tar.gz", hash = "sha256:5fb37580dcf4a262f9258c1f4373819aacca906431f505e4688e37f3a99195df"},
]

[package.dependencies]
asgiref = ">=3.7.0,<4"
sqlparse = ">=0.3.1"
tzdata = {version = "*", markers = "sys_platform == \"win32\""}

...Omitted
```

接着使用poetry导入requirements.txt重的项目。

```
> poetry add `cat requirements.txt`
Using version ^1.0.2 for pelican-markdown-include

Updating dependencies
Resolving dependencies... (12.9s)

Package operations: 44 installs, 0 updates, 0 removals

  - Installing idna (3.6)
  - Installing mdurl (0.1.2)
  - Installing sniffio (1.3.1)
  - Installing anyio (4.3.0)
  - Installing markdown-it-py (3.0.0)
  - Installing markupsafe (2.1.5)
  - Installing pygments (2.17.2)
  - Installing pytz (2024.1)
  - Installing six (1.16.0)
  - Installing blinker (1.7.0)
  - Installing docutils (0.20.1)
  - Installing feedgenerator (2.1.0)
  - Installing jinja2 (3.1.3)
  - Installing markdown (3.6)
  - Installing ordered-set (4.1.0)
  - Installing python-dateutil (2.9.0.post0)
  - Installing rich (13.7.1)
  - Installing smartypants (2.0.1)
  - Installing soupsieve (2.5)
  - Installing unidecode (1.3.8)
  - Installing watchfiles (0.21.0)
  - Installing webencodings (0.5.1)
  - Installing beautifulsoup4 (4.12.3)
  - Installing certifi (2024.2.2)
  - Installing charset-normalizer (3.3.2)
  - Installing html5lib (1.1)
  - Installing markdown-include (0.8.1)
  - Installing pelican (4.9.1)
  - Installing pelican-granular-signals (1.1.0)
  - Installing py3dns (4.0.1)
  - Installing tornado (6.4)
  - Installing typogrify (2.0.7)
  - Installing urllib3 (2.2.1)
  - Installing ghp-import (2.1.0)
  - Installing invoke (2.2.0)
  - Installing livereload (2.6.3)
  - Installing pelican-markdown-include (1.0.2)
  - Installing pelican-precompress (2.1.1)
  - Installing pelican-render-math (1.0.3)
  - Installing pelican-seo (1.2.2)
  - Installing pelican-simple-footnotes (1.0.2)
  - Installing pelican-sitemap (1.0.2)
  - Installing requests (2.31.0)
  - Installing zopfli (0.2.2)

Writing lock file
```

到这里就完成了`requirements.txt`的迁移，也可以安全的移除啦。

如果在这时需要更新一个软件的版本，则可以使用`poetry add <package>@latest`来进行安装。

```
> poetry add zopfli@latest
Using version ^0.2.3 for zopfli

Updating dependencies
Resolving dependencies... (0.5s)

Package operations: 0 installs, 1 update, 0 removals

  - Updating zopfli (0.2.2 -> 0.2.3)

Writing lock file
```

## poetry show

`poetry show`则是`pip show`的完全增强版。

你可以使用`-T`功能来显示所有顶层依赖。

```
> poetry show -T 
ghp-import               2.1.0       Copy your docs directly to the gh-pages branch.
invoke                   2.2.0       Pythonic task execution
livereload               2.6.3       Python LiveReload is an awesome tool for web developers
markdown-include         0.8.1       A Python-Markdown extension which provides an 'include' function
pelican                  4.9.1       Static site generator supporting Markdown and reStructuredText
pelican-markdown-include 1.0.2       Pelican plugin for using the Markdown-Include extension
pelican-photos           1.6.0       Add a photo or a gallery of photos to an article
pelican-precompress      2.2.0       Pre-compress your Pelican site using gzip, zopfli, and brotli!
pelican-render-math      1.0.3       Render mathematics in Pelican site content
pelican-seo              1.2.2       Pelican plugin to improve SEO (Search Engine Optimization) to reach top posit...
pelican-simple-footnotes 1.0.2       Pelican plugin to add footnotes to articles and pages
pelican-sitemap          1.1.0       Pelican plugin to generate sitemap in plain-text or XML format
requests                 2.31.0      Python HTTP for Humans.
zopfli                   0.2.3       Zopfli module for python
```

你可以使用`-t`选项来展示完整的项目依赖树。

```
> poetry show -t pelican
pelican 4.9.1 Static site generator supporting Markdown and reStructuredText
├── blinker >=1.7.0
├── docutils >=0.20.1
├── feedgenerator >=2.1.0
│   └── pytz >=0a 
├── jinja2 >=3.1.2
│   └── markupsafe >=2.0 
├── ordered-set >=4.1.0
├── pygments >=2.16.1
├── python-dateutil >=2.8.2
│   └── six >=1.5 
├── rich >=13.6.0
│   ├── markdown-it-py >=2.2.0 
│   │   └── mdurl >=0.1,<1.0 
│   └── pygments >=2.13.0,<3.0.0 
├── tzdata *
├── unidecode >=1.3.7
└── watchfiles >=0.21.0
    └── anyio >=3.0.0 
        ├── idna >=2.8 
        └── sniffio >=1.1 
```

你还可以使用`-o`选项来展示所有存在新版本的包。

```
> poetry show -o
pelican-precompress 2.1.1  2.2.0  Pre-compress your Pelican site using gzip, zopfli, and brotli!
pelican-sitemap     1.0.2  1.1.0  Pelican plugin to generate sitemap in plain-text or XML format
pillow              10.0.1 10.2.0 Python Imaging Library (Fork)
```

## poetry run

`Poetry`不仅包含了包管理系统，还提供了一个虚拟环境的管理。适用`poetry run <command>`命令等价于
```
(use virtual env)
<command>
(exit virtual env)
```

官方文档[Poetry Documentation - Managing environments](https://python-poetry.org/docs/managing-environments/)中记录了更多高阶的用法，这里笔者就不展开了。

## 小结

管理项目的依赖并不是一件容易的事情，而`poetry`可以安全的帮助我们解决重复劳作的问题。如果你的Python项目还在使用`requirements.txt`来管理包依赖的话，不妨花上10分钟升级一下，你会获得更好的体验。
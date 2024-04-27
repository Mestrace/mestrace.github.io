Title: 用 Python 进行代码覆盖率检测：coverage.py 和diff-cover 的使用方法
Slug: python-coverage-diff-cover
Date: 2023-02-05
Category: Computer Science
Tags: Python

在重构项目时，我们经常需要确认代码测试的覆盖率。这是为了确保没有任何部分遗漏或者错误，从而使重构变得更安全。为了帮助我们实现这一目标，我们可以使用两个 Python 包来帮助我们 `coverage.py` 和 `diff-cover`。

- `coverage.py`是一个代码插桩工具，它能够生成测试覆盖率报告。它的官方仓库是https://github.com/nedbat/coveragepy。
- `diff-cover`则是一个比对xml格式的coverage文件的工具，它能够将当前的覆盖率与origin/main或指定的commit进行比对。更多信息请参考它的官方仓库：https://github.com/Bachmann1234/diff_cover。

如果您的测试运行命令以`python`开头，只需要将初始的`python`替换为`coverage run`即可。
> If your test runner command starts with “python”, just replace the initial “python” with “coverage run”.
> 
> python something.py becomes coverage run something.py
> 
> python -m amodule becomes coverage run -m amodule


在运行完覆盖率的脚本之后，你的项目目录中会多出一个.coverage的元数据文件。为了使结果更加直观，我们需要将其进一步解析为更有说服力的形式。

使用 `coverage report --skip-covered --precision 2 --sort Cover` 命令，你可以在命令行窗口中看到每一个文件的覆盖率情况：

```bash
Name                             Stmts   Miss   Cover
-----------------------------------------------------
admin/models.py                      1      1   0.00%
admin/views.py                       1      1   0.00%
api/models.py                        1      1   0.00%
api/views.py                         1      1   0.00%
```

通过使用 `coverage html` 命令，你还可以在项目目录中生成一个html文档站，以查看更详细的覆盖率信息，以及覆盖了哪些代码行。

<p align="center">
  <img src="{static}/images/1/coverage_html.jpeg" />
</p>

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>


在对一个巨大的代码库进行修改之后，整个项目的覆盖率并不会有明显的改变，同时也很难定位关注点。为了确保我们的代码修改已经被覆盖到，我们需要提升测试用例的覆盖率，如果没有覆盖到的话，我们需要补充测试用例。有人可能说，这很简单，只需要对比目标分支和当前分支的差异，再去看对应行是否已经被测试覆盖了。幸运的是，已经有人为我们开发了一个工具diff-cover（https://pypi.org/project/diff-cover/ ）。使用coverage.py和diff-cover结合，我们可以迅速找到未被覆盖到的代码。

我们可以通过执行以下命令生成覆盖率报告：

```
coverage xml -o test.xml
```

然后，我们可以使用diff-cover读取该报告：

```
diff-cover test.xml --compare-branch origin/master --html-report diff-cover.html
```

其中，compare-branch参数需要指定用于与当前分支进行diff的分支，html-report参数则输出html格式的覆盖率报告。执行命令后，不仅会在命令行中输出类似如下的覆盖率信息：

```
-------------
Diff Coverage
Diff: origin/master...HEAD, staged and unstaged changes
-------------
account/controllers.py (76.5%): Missing lines 246,302,310,316
account/dao.py (90.3%): Missing lines 262,265,277
account/views.py (0.0%): Missing lines 179,187
-------------
Total:   50 lines
Missing: 9 lines
Coverage: 82%
-------------
```

还会生成一个包含具体代码覆盖行的html文档

<p align="center" width="50%" height="50%">
  <img src="{static}/images/1/diff_cover_html.jpeg" />
</p>

<p align="center">
  <img src="{static}/images/gei_li.png" />
</p>


在使用 `coverage.py` 进行代码测试覆盖率报告时，我们可能会遇到包含不必要文件和行的情况。例如，Django 自动生成的 `manage.py` 文件就不需要我们关注。同样地，代码行 `raise NotImplementedError` 也没有什么意义。因此，我们需要将它们屏蔽，以提高代码测试覆盖率报告的精度。

在运行 `coverage.py` 时，可以使用 `omit=[pattern1,pattern2…]` 选项忽略某些无关的文件，以及使用 `exclude_lines = [pattern1, pattern2]` 选项忽略某些无关的行。例如，使用命令 `coverage run --omit="tests" --source='.' manage.py test --keepdb` 可以忽略文件名包含 "tests" 的文件。

不过，每次都要手动输入 `omit` 和 `exclude-line` 选项非常麻烦，因此我们可以在项目根目录下配置 `.coveragerc` 文件，一次性配置所有选项。`.coveragerc` 文件使用 toml 格式编写，在运行 `coverage run / coverage report / coverage html` 命令时会读取其中的值并作为参数。

以下是我在 django 项目中使用的 `.coveragerc` 文件：


```
[run]
source = .
omit = ./venv/,*tests,apps.py,*manage.py,_init_.py,migrations,asgi,wsgi,*admin.py,*urls.py

[report]
omit = ./venv/,*tests,apps.py,*manage.py,_init_.py,migrations,asgi,wsgi,*admin.py,*urls.py
exclude_lines =
    pragma: no cover
    def _repr_
    if self.debug:
    if settings.DEBUG
    raise AssertionError
    raise NotImplementedError
    if 0:
    if _name_ == ._main_.:
    class .*\bProtocol\):
    @(abc\.)?abstractmethod
```

参考资料：

1. `coverage.py` 的官方文档 https://coverage.readthedocs.io/en/7.1.0/
2. `diff-cover` 的官方文档 https://diff-cover.readthedocs.io/en/latest/README.html
3. `.coveragerc` 文件来自 https://stackoverflow.com/questions/1628996/is-it-possible-exclude-test-directories-from-coverage-py-reports
4. `coverage.py` 的 Django 插件 https://pypi.org/project/django-coverage-plugin/

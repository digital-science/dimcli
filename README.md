# dimcli

> unofficial version, still in development

Python library for accessing the [Dimensions](https://www.dimensions.ai/) [DSL](https://app.dimensions.ai/dsl).

-   [https://github.com/lambdamusic/dimcli](https://github.com/lambdamusic/dimcli)
-   [https://pypi.org/project/dimcli/](https://pypi.org/project/dimcli/)

### Install

```
pip install dimcli
```

### Develop

Note: requires [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

```
$ mkvirtualenv dimcli
$ pip install --editable .
$ ./run-shell # iPython with library preloaded so you can play with it!
```

### Example

```
In [1]: import dimcli

In [2]: dimcli.Dsl('live', show_results=True, rich_display=False)
Out[2]: <dimcli.dimensions.Dsl at 0x10880a1d0>

In [3]: dsl = _

In [4]: dsl.query("search grants return grants")
```

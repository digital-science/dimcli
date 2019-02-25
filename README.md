# Dimcli

Python library for accessing the [Dimensions](https://www.dimensions.ai/) [DSL](https://app.dimensions.ai/dsl).

-   [https://github.com/lambdamusic/dimcli](https://github.com/lambdamusic/dimcli)
-   [https://pypi.org/project/dimcli/](https://pypi.org/project/dimcli/)

Dimcli includes a console-like tool that allows to launch queries against a Dimensions endpoint.

Main features:

-   autocomplete based on DSL grammar
-   history persists across sessions
-   displays query results as raw json or quick preview

> note: this library is an experimental project and still in development. Please report any bugs in the Github issues section.

### Install

```
pip install dimcli
```

Current version: see [pypi homepage](https://pypi.org/project/dimcli/).

### Running the CLI

Run the CLI by typing

```
dimcli
```

The only prerequisiste after installation is a configuration file with your Dimensions account credentials.

#### Credentials

This file must called `dsl.ini` and located in your user directory in the `.dimensions` folder. The contents must look like this:

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

In most situations you can simply copy/paste the text above and change the login and password as needed.

#### Multiple Dimensions Environments

If you have access to multiple Dimensions instances, you can just add more entries to the credentials files.

NOTE you can add details for more than one instance but make sure you give them unique names. So for example you can add another entry like this:

```
[instance.private]
url=https://local.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

Then when running the CLI you can select which instance to use just by passing its name as argument eg

```
dimcli private
```

> NOTE `live` is the instance name taken by default when no instance is specified.

### Using the library from Python

_TODO add more examples_

```
In [1]: import dimcli

In [2]: dsl = dimcli.Dsl('live', show_results=True, rich_display=False)
Out[2]: <dimcli.dimensions.Dsl at 0x10880a1d0>

In [3]: dsl.query("search grants return grants")
```

### Develop

Note: requires [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

```
$ mkvirtualenv dimcli
$ pip install --editable .
$ ./run-shell # launch iPython with library preloaded so you can play with it
```

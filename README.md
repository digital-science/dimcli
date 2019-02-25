# Dimcli

Python library for accessing the [Dimensions](https://www.dimensions.ai/) [DSL](https://app.dimensions.ai/dsl).

-   [https://github.com/lambdamusic/dimcli](https://github.com/lambdamusic/dimcli)
-   [https://pypi.org/project/dimcli/](https://pypi.org/project/dimcli/)

### Features

Dimcli includes a Command Line Interface tool that allows to launch queries against a Dimensions endpoint.

Main features:

-   autocomplete based on DSL grammar
-   history persists across sessions
-   displays query results as raw json or quick preview

> Development status: alpha.

Feedback's welcome, please use Github's [issues](https://github.com/lambdamusic/dimcli/issues/new).

### Install

```
$ pip install dimcli
```

Current version: see [pypi homepage](https://pypi.org/project/dimcli/).

Then you can check if the installation worked with

```
$ dimcli --help
```

### Running the CLI

Run the CLI by typing

```
$ dimcli
```

The only prerequisiste after installation is a configuration file with your Dimensions account credentials.

### Credentials File

This file must called `dsl.ini` and located in your user directory in the `.dimensions` folder. So this is what you'd do on unix systems:

```
$ mkdir ~/.dimensions
$ touch ~/.dimensions/dsl.ini
```

Then open `dsl.ini` and edit its contents. It should look like this:

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

In most situations you can simply copy/paste the text above and change the login and password as needed.

#### Multiple Dimensions Environments

If you have access to multiple Dimensions instances, you can just add more entries to the credentials files.

You can add details for more than one instance but make sure you give them unique names. So for example you can add another entry like this:

```
[instance.private]
url=https://private-instance.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

Then when running the CLI you can select which instance to use just by passing its name as argument eg

```
$ dimcli private
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


- [Dimcli](#dimcli)
    - [In a nutshell](#in-a-nutshell)
  - [Installation](#installation)
      - [Anaconda users](#anaconda-users)
  - [Authentication](#authentication)
    - [Creating a credentials file using the helper script (recommended)](#creating-a-credentials-file-using-the-helper-script-recommended)
    - [Creating a credentials file manually](#creating-a-credentials-file-manually)
    - [Overriding credentials at runtime (e.g. with Jupyter Notebooks)](#overriding-credentials-at-runtime-eg-with-jupyter-notebooks)
    - [Using multiple API endpoints (for advanced users)](#using-multiple-api-endpoints-for-advanced-users)
  - [Dimcli as a Command Line Interface](#dimcli-as-a-command-line-interface)
  - [Dimcli with Jupyter Notebooks](#dimcli-with-jupyter-notebooks)
  - [Dimcli as a Python module](#dimcli-as-a-python-module)
  - [Comments, bug reports](#comments-bug-reports)


# Dimcli

### In a nutshell

Dimcli is a Python client for accessing the [Dimensions Analytics API](https://www.dimensions.ai/). It makes it easier to authenticate against the API, send queries to it and process the JSON data being returned.  

Dimcli includes also a command line interface (CLI) that aims at simplifying the process of learning the grammar of the Dimensions Search Language ([DSL](https://app.dimensions.ai/dsl)). Calling `dimcli` from the terminal opens an interactive query console with syntax autocomplete, persistent history across sessions, pretty-printing and preview of JSON results, export to HTML and CSV, and more.  

![dimcli_animation](https://raw.githubusercontent.com/digital-science/dimcli/master/static/dimcli_animated.gif)

Current version: see [pypi homepage](https://pypi.org/project/dimcli/). Source code hosted on [github](https://github.com/digital-science/dimcli). An older animated video on [asciicinema](https://asciinema.org/a/jSzISIsaXN2VbpOApSSOSwGcj).



## Installation

Install / upgrade the package as follows:

```
$ pip install dimcli -U
```

Then you can check if the installation worked with

```
$ dimcli --help
```

#### Anaconda users

There's been [reports](https://github.com/digital-science/dimcli/issues/21) of Dimcli failing to install on Anacoda. This can be solved by updating manually a couple of libraries Dimcli relies on:
* `pip install prompt-toolkit -U` 
* `pip install ipython -U` 



## Authentication 


After installation it's **strongly advised to create a configuration file** with your Dimensions account credentials. This can be done only once, and it'll save you from having to type in credentials each time you use DimCli. E.g. 

```
>>> import dimcli
>>> dimcli.login() # config file is picked up automatically 
```

If you can't create a configuration file you can explicitly provide log in credentials as follows (see also the [Python section](#dimcli-as-a-python-module) for more options).

```
>>> import dimcli

# you can specify endpoint, which by default is set to "https://app.dimensions.ai"
>>> dimcli.login(user="mary.poppins", 
                 password="chimneysweeper", 
                 endpoint="https://app.dimensions.ai")

```


### Creating a credentials file using the helper script (recommended)

The easiest way to set up the authentication file is to use the command line helper: 

```
$ dimcli --init
```

The helper will guide you through the process of creating this file, which will be safely stored in your computer home folder. That's it - you're ready to hit the API! See below for more info on how to do that.


### Creating a credentials file manually

This section provides more details about where DimCli expects credentials data to be found, in case you want to set this up manually. 

The credentials file must be called `dsl.ini` and located in your user directory in the `.dimensions` folder. If you want to set this up manually, this is what you'd do on unix systems:

```
$ mkdir ~/.dimensions
$ touch ~/.dimensions/dsl.ini
```

Then open `dsl.ini` with a text editor. Its contents should look like this:

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

In most situations you can simply copy/paste the text above and change the login and password as needed.

> Note: you must always have an entry in the configuration called `[instance.live]`


### Overriding credentials at runtime (e.g. with Jupyter Notebooks)

If you are using DimCli within a Jupyter notebook and you do not want (or can) set up credentials at the user level, you can simply put a `dsl.ini` file in the current working directory (= where the notebook is located).  

The file should look like this:

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

> Note: the same-directory credentials will take precedence over any system-level credentials previously defined.


### Using multiple API endpoints (for advanced users)

If you have access to multiple Dimensions API endpoints (or instances), you can just add more entries to the credentials file.

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



## Dimcli as a Command Line Interface

DimCli includes a handy Command Line Interface (CLI) which lets you query the Dimensions API interactively. The CLI has several features but, most importantly, it allows to use the TAB key to autocomplete your queries (based on the latest API syntax and fields), which makes it an ideal tool for both newbies and expert users.  

Run the command line application by typing

```
$ dimcli
```

That'll launch the DimCli console, where you can hit `help` in case you need more support :-)

![screenshot1](static/screenshot1.jpg)


## Dimcli with Jupyter Notebooks

DimCli includes a number of features that simplify working with the Dimensions API within a Jupyter notebook. 

For example, it contains a couple of [magic commands](https://github.com/digital-science/dimcli/blob/master/dimcli/jupyter/magics.py) that make it super easy to hit the API from a notebook, or to explore the documentation. 

For more information and examples see the notebooks available in the official [Dimensions API Lab](https://github.com/digital-science/dimensions-api-lab) repository.


## Dimcli as a Python module

Dimcli can be used as a wrapper around the Dimensions API within a Python program. It makes it easier to authenticate, query the Dimensions endpoint and handle the results, normally returned as JSON. 

```
>>> import dimcli

# if you have already set up the credentials file (see above), no need to pass log in details
>>> dimcli.login()

# otherwise you can authenticate by passing your login details as arguments
>>> dimcli.login(user="mary.poppins", password="chimneysweeper")

# you can specify endpoint, which by default is set to "https://app.dimensions.ai"
>>> dimcli.login(user="mary.poppins", password="chimneysweeper", ednpoint="https://nannies-research.dimensions.ai")

```

Once logged in, you can get a query object and try some queries:

```

>>> dsl = dimcli.Dsl()

# queries always return a Dataset object (subclassing IPython.display.JSON)
>>> dsl.query("search grants for \"malaria\" return publications")
<dimcli.dimensions.Dataset object>

# use the .data method to get the JSON
>>> dsl.query("search grants for \"malaria\" return publications").data
{'errors': {'query': {'header': 'Semantic Error',
   'details': ["Semantic errors found:\n\tFacet 'publications' is not present in source 'grants'. Available facets are: FOR,FOR_first,HRCS_HC,HRCS_RAC,RCDC,active_year,funder_countries,funders,funding_org_acronym,funding_org_city,funding_org_name,language,research_org_cities,research_org_countries,research_org_name,research_org_state_codes,research_orgs,researchers,start_year,title_language"],
   'query': 'search grants for "malaria" return publications'}}}

# now a good query
>>> res = dsl.query("search grants for \"malaria\" return researchers")
>>> print(res.data)
{'researchers': [{'id': 'ur.01332073522.49',
   'count': 75,
   'last_name': 'White',
   'first_name': 'Nicholas J'},
  {'id': 'ur.01343654360.43',
   'count': 59,
   'last_name': 'Marsh',
   'first_name': 'Kevin'},
  .............
  ],
 '_stats': {'total_count': 8735}}

# JSON keys are available also as dict attributes
>>> res['researchers'][0] 
{'id': 'ur.01332073522.49',
 'count': 75,
 'last_name': 'White',
 'first_name': 'Nicholas John'}
# note: res.['researchers'] is also allowed!

# so now let's pull out all names and surnames
>>> [x['first_name'] + " " + x['last_name'] for x in res['researchers']]
['Nicholas John White',  'Kevin Marsh',
 'Nicholas Philip John Day', 'Takafumi Tsuboi',
 'Malcolm Edward Molyneux', 'Kazuyuki Tanabe',
 'Stephen Lev Hoffman', 'Toshihiro Horii',
 'Louis H Miller', 'Francois Henri Nosten',
 'Motomi Torii', 'Alan Frederick Cowman',
 'Patrick Emmet Duffy', 'Satoru Kawai',
 'Alister Gordon Craig', 'Fumihiko Kawamoto',
 'Makoto Hirai', 'Marcelo Urbano Ferreira',
 'Osamu Kaneko', 'Yusuke Wataya']

```

## Comments, bug reports

Dimcli lives on [Github](https://github.com/digital-science/dimcli/). You can file [issues]([issues](https://github.com/digital-science/dimcli/issues/new)) or pull requests there. Suggestions, pull requests and improvements welcome!
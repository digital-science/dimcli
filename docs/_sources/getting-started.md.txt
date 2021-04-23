
# Getting Started with Dimcli

### In a nutshell

Dimcli is a Python client for accessing the [Dimensions Analytics API](https://www.dimensions.ai/). It makes it easier to authenticate against the API, send queries to it and process the JSON data being returned. E.g.:


```
>>> import dimcli

>>> dimcli.login(user="mary.poppins", password="chimneysweeper")

>>> dsl = dimcli.Dsl()

>>> res = dsl.query("""search grants for "malaria" return researchers""")

>>> print(res.json)
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


```

Dimcli includes also a **command line interface** (CLI) that aims at simplifying the process of learning the grammar of the Dimensions Search Language ([DSL](https://app.dimensions.ai/dsl)). Calling `dimcli` from the terminal opens an interactive query console with syntax autocomplete, persistent history across sessions, pretty-printing and preview of JSON results, export to HTML and CSV, and more.  

![dimcli_animation](https://raw.githubusercontent.com/digital-science/dimcli/master/static/dimcli_animated.gif)

Current version: see [pypi homepage](https://pypi.org/project/dimcli/). 
Source code hosted on [github](https://github.com/digital-science/dimcli). 
See also an older animated video on [asciicinema](https://asciinema.org/a/jSzISIsaXN2VbpOApSSOSwGcj).



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


After installation it's **strongly advised to create a configuration file** containing your Dimensions account credentials. This can be done only once and it'll save you from having to type in credentials each time you use Dimcli. E.g. 

```
>>> import dimcli
>>> dimcli.login() # config file is picked up automatically 
```

If you can't create a configuration file you can explicitly provide log in credentials as follows (see also the [Dimcli as a Python module](#dimcli-as-a-python-module) section for more options).

```
>>> import dimcli

# you can specify endpoint, which by default is set to "https://app.dimensions.ai"
>>> dimcli.login(user="mary.poppins", 
                 password="chimneysweeper", 
                 endpoint="https://app.dimensions.ai")

```

Or if you are using **key-based** authentication: 

```
>>> import dimcli

>>> dimcli.login(key="123456789qwertyuiop",  
                 endpoint="https://https://my.instance.of.dimensions.ai")

```


### Creating a credentials file using the helper script (recommended)

The easiest way to set up the authentication file is to use the command line helper: 

```
$ dimcli --init
```

The helper will guide you through the process of creating this file, which will be safely stored in your computer home folder. That's it - you're ready to hit the API! See below for more info on how to do that.


### Creating a credentials file manually

This section provides more details about where Dimcli expects credentials data to be found, in case you want to set this up manually. 

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
key=yourkeyhere
```

In most situations you can simply copy/paste the text above and update its contents as needed. 

#### Important

* you must always have an entry in the credentials file called `[instance.live]`
* depending on whether you authenticate using an API key or username & password, fill in the relevant details and just leave the other stuff blank. Eg this is a valid config snippet if you authenticate using a key:

```
[instance.live]
url=https://app.dimensions.ai
login=
password=
key=yourkeyhere
```




### Overriding credentials at runtime (e.g. with Jupyter Notebooks)

If you are using Dimcli within a Jupyter notebook and you do not want (or cannot) set up credentials globally, you can simply put a `dsl.ini` file in the current working directory (= where the notebook is located).  

The file contents should look just like above, that is:

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
key=yourkeyhere
```

**Note** the same-directory credentials will take precedence over any system-level credentials previously defined.


### Using multiple API endpoints (for advanced users)

If you have access to multiple Dimensions API endpoints (or instances), you can just add more entries to the credentials file.

You can add details for more than one instance but make sure you give them unique names. So for example you can add another entry like this:

```
[instance.private]
url=https://private-instance.dimensions.ai
login=user@mail.com
password=yourpasswordhere
key=yourkeyhere
```

Then when running the CLI you can select which instance to use just by passing its name as argument eg

```
$ dimcli private
```


## Settings

A settings file can be stored alongside the authentication details file, in order to enable other functionalities. 

This file must be called `settings` and it has to be located in your user directory, in the `.dimensions` folder. This is what you'd do on unix systems:

```
$ touch ~/.dimensions/settings
```


### Github Gists Token

By adding a github authentication [token](https://github.com/settings/tokens) to the settings file, it is possible to save API query results to [https://gist.github.com/](https://gist.github.com/). 

See this guide on [how to create a new token](https://docs.github.com/en/free-pro-team@latest/github/authenticating-to-github/creating-a-personal-access-token). Ensure that the token has the 'gists' scope from the available options. 

One you have the token, add the following section to the `settings` file (of course replacing the token value with your token): 

```
[gist]
token: d5047fASAD889912HHBAJVSAD8e8bae17e2
```

This will allow to export/create gists from DSL queries when using the Dimcli CLI. 

> NOTE: all gists created by Dimcli are not private to your Github account (=unlisted)



## Dimcli as a Python module

Dimcli can be used as a wrapper around the Dimensions API within a Python program. It makes it easier to authenticate, query the Dimensions endpoint and handle the results, normally returned as JSON. 

```
>>> import dimcli

# if you have already set up the credentials file (see above), no need to pass log in details
>>> dimcli.login()

# you can pass explicitly your login details as arguments
>>> dimcli.login(key="my-super-secret-key", endpoint="https://app.dimensions.ai")

# works also with the legacy authentication method
>>> dimcli.login(username="mary.poppins", password="chimneysweeper")

# if your account uses a different endpoint, you can specify that 
>>> dimcli.login(username="mary.poppins", password="chimneysweeper", endpoint="https://nannies-research.dimensions.ai")

```

Once logged in, you can get a query object and try some queries:

```

>>> dsl = dimcli.Dsl()

# queries always return a DslDataset object (subclassing IPython.display.JSON)
>>> dsl.query("search grants for \"malaria\" return publications")
<dimcli.dimensions.DslDataset object>

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

The [Dimensions API Lab](https://api-lab.dimensions.ai/) includes several notebooks demonstrating the practical use of Dimcli. In particular, these two are a good place to start: 

* [The Dimcli Python library: Installation and Querying](https://api-lab.dimensions.ai/cookbooks/1-getting-started/1-Using-the-Dimcli-library-to-query-the-API.html)
* [The Dimcli Python library: Working with Pandas Dataframes](https://api-lab.dimensions.ai/cookbooks/1-getting-started/3-Working-with-dataframes.html)



## Dimcli as a Command Line Interface

Dimcli includes a handy Command Line Interface (CLI) which lets you query the Dimensions API interactively. The CLI has several features but, most importantly, it allows to use the TAB key to autocomplete your queries (based on the latest API syntax and fields), which makes it an ideal tool for both newbies and expert users.  

Run the command line application by typing

```
$ dimcli
```

That'll launch the Dimcli console, where you can hit `help` in case you need more support :-)

![dimcli_animation](https://raw.githubusercontent.com/digital-science/dimcli/master/static/dimcli_animated.gif)



## Dimcli with Jupyter Notebooks

Dimcli includes a number of features that simplify working with the Dimensions API within Jupyter notebooks. 

For example, it contains a few [magic commands](https://github.com/digital-science/dimcli/blob/master/dimcli/jupyter/magics.py) that make it super-easy to hit the API from a notebook cell:


* `%dsl` can be used to run an API query
* `%dslloop` can be used to run an API query, using pagination (= iterations up to 50k records)
* `%dsldf` can be used to run an API query and transform the JSON data to a dataframe
* `%dslloopdf` can be used to run a paginated API query and transform the JSON data to a dataframe
* `%dsldocs` can be used to programmatically extract API schema information

For more information and examples see the [The Dimcli Python library: Magic Commands](https://api-lab.dimensions.ai/cookbooks/1-getting-started/4-Dimcli-magic-commands.html) notebook and the [jupyter.magics module](https://digital-science.github.io/dimcli/modules.html#module-dimcli.jupyter.magics).

## Changelog

See the file `CHANGELOG.md` on [Github](https://github.com/digital-science/dimcli) - [https://github.com/digital-science/dimcli/blob/master/CHANGELOG.md](https://github.com/digital-science/dimcli/blob/master/CHANGELOG.md)


## Comments, bug reports

Dimcli lives on [Github](https://github.com/digital-science/dimcli/). You can file [issues](https://github.com/digital-science/dimcli/issues/new) or pull requests there. Suggestions, pull requests and improvements welcome!
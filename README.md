
- [Dimcli](#dimcli)
    - [In a nutshell](#in-a-nutshell)
  - [Installation](#installation)
      - [Authentication](#authentication)
      - [The Credentials File](#the-credentials-file)
      - [Advanced: Multiple API Endpoints](#advanced-multiple-api-endpoints)
      - [Overriding credentials at runtime e.g. with Jupyter Notebooks](#overriding-credentials-at-runtime-eg-with-jupyter-notebooks)
  - [Using DimCli as a CLI](#using-dimcli-as-a-cli)
  - [Using Dimcli as a Python library](#using-dimcli-as-a-python-library)
  - [Using Dimcli in Jupyter Notebooks](#using-dimcli-in-jupyter-notebooks)
  - [Comments, bug reports](#comments-bug-reports)


# Dimcli

[![asciicast](https://asciinema.org/a/jSzISIsaXN2VbpOApSSOSwGcj.svg)](https://asciinema.org/a/jSzISIsaXN2VbpOApSSOSwGcj)


### In a nutshell

Dimcli is a Python library for accessing the [Dimensions Analytics API](https://www.dimensions.ai/). It makes it easier to authenticate, query the API endpoint and process the results, normally returned as JSON. 

Dimcli provides an interactive environment which aims at simplifying the process of learning the grammar of the Dimensions Search Language ([DSL](https://app.dimensions.ai/dsl)). Calling `dimcli` from the terminal opens a CLI featuring autocomplete (based on the DSL syntax and vocabulary), persistent history across sessions, pretty-printing and preview of JSON results, export to HTML and CSV, and more.  

Current version: see [pypi homepage](https://pypi.org/project/dimcli/). Source code hosted on [github](https://github.com/lambdamusic/dimcli).


## Installation

```
$ pip install dimcli -U
```

Then you can check if the installation worked with

```
$ dimcli --help
```

#### Authentication 


After installation it's strongly advised to create a configuration file with your Dimensions account credentials. This can be done only once, and it'll save you from having to authenticate each time you use DimCli. 

The easiest way to set up the authentication file is to use the command line helper: 

```
$ dimcli --init
```

The helper will guide you through the process of creating this file, which will be safely stored in your computer home folder. That's it - you're ready to hit the API! See below for more info on how to do that.


#### The Credentials File

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

#### Advanced: Multiple API Endpoints

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


#### Overriding credentials at runtime e.g. with Jupyter Notebooks

If you are using DimCli within a jupyter notebook and you do not want (or can) set up credentials at the user level, you can simply put a `dsl.ini` file in the current working directory (= where the notebook is located).  

The file should look like this:

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```

> Note: the same-directory credentials will take precedence over any system-level credentials previously defined.



## Using DimCli as a CLI 

DimCli includes a handy CLI which lets you query the Dimensions API interactively. The CLI has several features but, most importantly, it allows to use the TAB key to autocomplete your queries (based on the latest API syntax and fields), which makes it an ideal tool for both newbies and expert users.  

Run the command line application by typing

```
$ dimcli
```

That'll launch the DimCli console, where you can hit `help` in case you need more support :-)

![screenshot1](static/screenshot1.jpg)


## Using Dimcli as a Python library

Dimcli can be used as a wrapper around the Dimensions API within a Python program. It makes it easier to authenticate, query the Dimensions endpoint and handle the results, normally returned as JSON. 

```
>>> import dimcli

# if you have already set up the credentials file (see above), no need to pass log in details
>>> dsl = dimcli.Dsl()

# otherwise you can authenticate by passing your login details as arguments
>>> dsl = dimcli.Dsl(user="mary.poppins", password="chimneysweeper")

# you can specify endpoint, which by default is set to "https://app.dimensions.ai"
>>> dsl = dimcli.Dsl(user="mary.poppins", password="chimneysweeper", ednpoint="https://nannies-research.dimensions.ai")
```

Once logged in, you can try some queries:

```
# queries always return a Result object (subclassing IPython.display.JSON)
>>> dsl.query("search grants for \"malaria\" return publications")
<dimcli.dimensions.Result object>

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

## Using Dimcli in Jupyter Notebooks

DimCli can simplify working with the Dimensions API within a Jupyter notebook. For example, it contains a couple of Python _magic_ commands that make it super easy to hit the API from a notebook. 

> this section of the docs is still being finished, but you can see DimCli in action in this [repo](https://github.com/digital-science/dimensions-api)


## Comments, bug reports

Dimcli lives on [Github](https://github.com/lambdamusic/dimcli/). You can file [issues]([issues](https://github.com/lambdamusic/dimcli/issues/new)) or pull requests there. Suggestions, pull requests and improvements welcome!
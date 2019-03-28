
- [Dimcli](#dimcli)
    - [In a nutshell](#in-a-nutshell)
  - [Install](#install)
  - [Using the Query Console](#using-the-query-console)
      - [The Credentials File](#the-credentials-file)
      - [Advanced: Multiple API Endpoints](#advanced-multiple-api-endpoints)
      - [Overriding credentials e.g. with Jupyter Notebooks](#overriding-credentials-eg-with-jupyter-notebooks)
  - [Using Dimcli as a Python library](#using-dimcli-as-a-python-library)
  - [Comments, bug reports](#comments-bug-reports)


# Dimcli

[![asciicast](https://asciinema.org/a/jSzISIsaXN2VbpOApSSOSwGcj.svg)](https://asciinema.org/a/jSzISIsaXN2VbpOApSSOSwGcj)

Python library for accessing the [Dimensions](https://www.dimensions.ai/) API. See the video above for a quick demo. 

-   [https://github.com/lambdamusic/dimcli](https://github.com/lambdamusic/dimcli)
-   [https://pypi.org/project/dimcli/](https://pypi.org/project/dimcli/)

### In a nutshell

Dimcli is a small Python wrapper around the Dimensions API. It makes it easier to authenticate, query the Dimensions endpoint and handle the results, normally returned as JSON. 

Dimcli also provides an interactive environment for learning about the Dimensions Search Language ([DSL](https://app.dimensions.ai/dsl)). Calling `dimcli` from the shell opens a console-like tool with many features such as autocomplete based on DSL grammar, persistent history across sessions, pretty-printing or previewing of JSON results, and more.  

Current version: see [pypi homepage](https://pypi.org/project/dimcli/).


## Install

```
$ pip install dimcli -U
```

Then you can check if the installation worked with

```
$ dimcli --help
```

## Using the Query Console

Run the command line application by typing

```
$ dimcli
```

The only prerequisiste after installation is a configuration file with your Dimensions account credentials. These can be set up directly from the command line by typing:

```
$ dimcli --init
```

For more info see the following section.

#### The Credentials File

The credentials file must be called `dsl.ini` and located in your user directory in the `.dimensions` folder. So if yoy want to set this up manually, this is what you'd do on unix systems:

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


#### Overriding credentials e.g. with Jupyter Notebooks

If you are using dimcli within a jupyter notebook and you do not want (or can) set up credentials at the user level, you can simply but a `dsl.ini` file in the current working directory (eg where the notebooks are located).  

These credentials will take precedence over any other file previously defined.

```
[instance.live]
url=https://app.dimensions.ai
login=user@mail.com
password=yourpasswordhere
```


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
  {'id': 'ur.013570515662.78',
   'count': 39,
   'last_name': 'Day',
   'orcid_id': ['0000-0003-2309-1171'],
   'first_name': 'Nicholas P  J'},
  {'id': 'ur.01246255474.14',
   'count': 32,
   'last_name': 'Tsuboi',
   'first_name': 'Takafumi'},
  {'id': 'ur.013621403537.53',
   'count': 32,
   'last_name': 'Molyneux',
   'orcid_id': ['0000-0002-7093-8921'],
   'first_name': 'Malcolm E'},
  {'id': 'ur.0646650127.76',
   'count': 32,
   'last_name': 'Tanabe',
   'first_name': 'Kazuyuki'},
  {'id': 'ur.01004335615.66',
   'count': 29,
   'last_name': 'Hoffman',
   'first_name': 'Stephen L'},
  {'id': 'ur.01013145443.28',
   'count': 29,
   'last_name': 'Horii',
   'first_name': 'Toshihiro'},
  {'id': 'ur.011050223772.27',
   'count': 29,
   'last_name': 'Miller',
   'orcid_id': ['0000-0003-3420-1284'],
   'first_name': 'Louis H'},
  {'id': 'ur.07764267264.89',
   'count': 29,
   'last_name': 'Nosten',
   'orcid_id': ['0000-0002-7951-0745'],
   'first_name': 'Francois'},
  {'id': 'ur.01200142274.58',
   'count': 28,
   'last_name': 'Torii',
   'first_name': 'Motomi'},
  {'id': 'ur.01157022450.71',
   'count': 25,
   'last_name': 'Cowman',
   'orcid_id': ['0000-0001-5145-9004'],
   'first_name': 'Alan F'},
  {'id': 'ur.01231001203.23',
   'count': 25,
   'last_name': 'Duffy',
   'first_name': 'Patrick E'},
  {'id': 'ur.01370151200.33',
   'count': 24,
   'last_name': 'Kawai',
   'first_name': 'Satoru'},
  {'id': 'ur.014032733622.20',
   'count': 24,
   'last_name': 'Craig',
   'orcid_id': ['0000-0003-0914-6164'],
   'first_name': 'Alister G'},
  {'id': 'ur.01123513136.18',
   'count': 23,
   'last_name': 'Kawamoto',
   'first_name': 'Fumihiko'},
  {'id': 'ur.010634112405.45',
   'count': 22,
   'last_name': 'Hirai',
   'first_name': 'Makoto'},
  {'id': 'ur.0612737310.86',
   'count': 22,
   'last_name': 'Ferreira',
   'orcid_id': ['0000-0002-5293-9090'],
   'first_name': 'Marcelo U'},
  {'id': 'ur.0725323667.50',
   'count': 22,
   'last_name': 'Kaneko',
   'first_name': 'Osamu'},
  {'id': 'ur.013471271621.48',
   'count': 21,
   'last_name': 'Wataya',
   'first_name': 'Yusuke'}],
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
['Nicholas John White',
 'Kevin Marsh',
 'Nicholas Philip John Day',
 'Takafumi Tsuboi',
 'Malcolm Edward Molyneux',
 'Kazuyuki Tanabe',
 'Stephen Lev Hoffman',
 'Toshihiro Horii',
 'Louis H Miller',
 'Francois Henri Nosten',
 'Motomi Torii',
 'Alan Frederick Cowman',
 'Patrick Emmet Duffy',
 'Satoru Kawai',
 'Alister Gordon Craig',
 'Fumihiko Kawamoto',
 'Makoto Hirai',
 'Marcelo Urbano Ferreira',
 'Osamu Kaneko',
 'Yusuke Wataya']

```


## Comments, bug reports

Dimcli lives on [Github](https://github.com/lambdamusic/dimcli/). You can file [issues]([issues](https://github.com/lambdamusic/dimcli/issues/new)) or pull requests there. Suggestions, pull requests and improvements welcome!
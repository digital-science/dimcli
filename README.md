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


### Install

```
$ pip install dimcli -U
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

The only prerequisiste after installation is a configuration file with your Dimensions account credentials. These can be set up directly from the command line by typing:

```
$ dimcli --init
```

For more info see the following section.

### Credentials File

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

# if you have set up a credentials file, no need to pass log in details
In [2]: dsl = dimcli.Dsl()

# queries always return a Result object (subclassing IPython.display.JSON)
In [3]: dsl.query("search grants for \"malaria\" return publications")
Out[3]: <dimcli.dimensions.Result object>

# use the .data method to get the JSON
In [4]: dsl.query("search grants for \"malaria\" return publications").data
Out[4]:
{'errors': {'query': {'header': 'Semantic Error',
   'details': ["Semantic errors found:\n\tFacet 'publications' is not present in source 'grants'. Available facets are: FOR,FOR_first,HRCS_HC,HRCS_RAC,RCDC,active_year,funder_countries,funders,funding_org_acronym,funding_org_city,funding_org_name,language,research_org_cities,research_org_countries,research_org_name,research_org_state_codes,research_orgs,researchers,start_year,title_language"],
   'query': 'search grants for "malaria" return publications'}}}

# now a good query
In [5]: res = dsl.query("search grants for \"malaria\" return researchers")
In [6]: res.data
Out[6]:
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

# JSON keys are available as slice objects or attributes
In [7]: res.researchers[0] 
Out[7]:
{'id': 'ur.01332073522.49',
 'count': 75,
 'last_name': 'White',
 'first_name': 'Nicholas John'}
# note: res.['researchers'] is also allowed!

# so now let's pull out all names and surnames
In [8]: [x['first_name'] + " " + x['last_name'] for x in res.researchers]
Out[8]:
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

### Develop

Note: requires [virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/).

```
$ mkvirtualenv dimcli
$ pip install --editable .
$ ./run-shell # launch iPython with library preloaded so you can play with it
```


### Comments, bug reports

Dimcli lives on [Github](https://github.com/lambdamusic/dimcli/). You can file [issues]([issues](https://github.com/lambdamusic/dimcli/issues/new)) or pull requests there. Suggestions, pull requests and improvements welcome!
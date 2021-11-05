# Dimcli

Dimcli is a Python client for accessing the Dimensions Analytics API. It makes it easier to authenticate against the API, send queries to it and process the JSON data being returned.  

```bash
>>> import dimcli

>>> dimcli.login(key="private-key-here",  
                 endpoint="https://app.dimensions.ai/api/dsl/v2")
               
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

Dimcli includes also a command line interface (CLI) that aims at simplifying the process of learning the grammar of the Dimensions Search Language (DSL).

![dimcli_animation](https://raw.githubusercontent.com/digital-science/dimcli/master/static/dimcli_animated.gif)

For more information see the [Getting Started with Dimcli](https://digital-science.github.io/dimcli/getting-started.html) tutorial.

Current version: see [pypi homepage](https://pypi.org/project/dimcli/). Source code hosted on [github](https://github.com/digital-science/dimcli). 

[![Downloads](https://pepy.tech/badge/dimcli)](https://pepy.tech/project/dimcli)


## Comments, bug reports

Dimcli lives on [Github](https://github.com/digital-science/dimcli/). You can file [issues]([issues](https://github.com/digital-science/dimcli/issues/new)) or pull requests there. Suggestions, pull requests and improvements welcome!

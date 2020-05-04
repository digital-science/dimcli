# Changelog


## v 0.6.7

* support for `_version` info in payload
* shortcut for grants results: `df_grant_investigators_affiliations` 
* pretty printing for repl `.json_compact` command
* `dsl_escape` accepts boolean arg for escaping any special character (by default it escapes only `"`)


## v 0.6.6

* CLI: new categories autocomplete, for Units of Assesment and Sustainable Development Goals
* CLI: barchart export `export_as_bar_chart`
* CLI: html export includes API endpoint information, for better traceability
* `Dataset.as_dataframe_concepts()` method: improved metrics and performance


## v 0.6.5

* remove legacy `Dsl.login()` method (should use `dimcli.login` instead) 
* fixed BUG in repl that prevented autocompletion of non-filter fields
* remove Warning by updating `pandas.json_normalize` import
* project docs via sphinx 
* CLI command `record_notebook` turns latest queries into jupyter notebook

## v 0.6.4

* grammar for new source `Datasets`
* improved `dsl_escape` method desc, when a query with quotes needs to be escaped

## v 0.6.3

* Refactor command line options. Try it with `dimcli -h`
* New command for resolving Dimensions IDs into URLs `dimcli -id [value]`
* Grammar for DSL V 1.22
* Refactor login: invalid credentials raise an error (previously just a message)
* Refactor query_iterative: error while looping provides better infos

## v 0.6.2 

* `dimcli.Dataset`  is the new name of dimcli.Result  and is available at module level
* methods to build `Dataset` from raw data (instead of from a query) so to reuse as_dataframe() methods etc:  `Dataset.from_publications_list(data)` 
  * data can be from list of dictionaries
  * or data can be a dataframe (eg obtained from previous query operations)
* experimental feature `Dataset.as_dimensions_url()` 
* `dimcli.login()` method now accepts an optional argument `verbose=True/False` to enable/suppress feedback 
* `Dsl.query_iterative` takes an extra argument `pause` determining iteration break length (default = 1.5 seconds)
* added more utility functions to `dimcli.shortcuts` module 
* new method `Dataset.as_dataframe_concepts()` for publications and grants. Returns a full list of all concepts, including position, score (in the context of a publication/grant) and frequency (across records).

* fixed error with `as_dataframe_investigators` 
* fixed error with `limit` keyword wrongly found in iterative_query
* fixed error with verbose flag lost after queries with 403s or automatic retries
* improved autocomplete after magic command %dsl 



## v 0.6.1 

* fix for double-printed error messages in CLI
* removed deprecated magic commands 
* improved printouts on magic methods 
* ensuring magic methods with dataframe work only with `search` queries 


## v 0.6

* Query Warnings and Error messages printed out by default in Jupyter environments
* Added `verbose` option to suppress all messages (default = True)
  * `dsl = dimcli.Dls(verbose=False)`: global 
  * `dsl.query(q, verbose=False)`: local for a specific query
* Improved `query_iterative` to handle max 50k results and timeouts (from too many queries)
* Refactored CLI module and imports 


## v 0.5.9

* `dsl_escape` util
* `api.Result.errors` helper method
* improved integration with Google Colab
  * `%load_ext google.colab.data_table` ran by default
* CLI: improved autocomplete with `[fieldname1+fieldname2]` syntax
* cleanup of `Dsl` object


## v 0.5.8

* dimcli CLI
  * simplified html output of `export_as_html` command
  * '.show_json_compact' and '.show_json_full' commands renamed to `.json_compact` and `.json_full`
* removed `json2html` dependency 
* couple of utility methods for data analysis
  * dimcli.core.utils.dimensions_url for generating valid Dimensions webapp URLs from object IDs
  * dimcli.core.utils.google_url for generating a google search URL from a string
* command line utils to check if a newer version of the library is available
  * `dimcli -v` or `dimcli --versioncheck`
  * run by default when CLI starts as well
* query results exports now go to `~/dimcli-exports` folder (instead of `.dimensions`) 


## v 0.5.7

* downgraded dependencies versions, to allow Dimcli to work better with [Google Colab](https://colab.research.google.com/)
  * `ipython >=5.5.0`, `prompt-toolkit>=1.0.16`  (instead of `ipython>=7.2.0`, `prompt-toolkit>=2.0.9`)
  * users of the CLI can upgrade on demand 
* CLI has now autocomplete on category fields: `category_rcdc`, `category_hrcs_rac`, `category_hrcs_hc`, `category_hra`, `category_bra`, `category_for`


## v 0.5.6.2

* fixed bug with dimcli shell
* fixed issue with UTF-8 encoding of queries

## v 0.5.6

* refactored login approach: `dimcli.login(username, password)` is now the main method that should be used
* various improvements to ensure dimcli login works seamlessly in jupyter notebooks 
* refactored magic command names `%dsl`, `%dslloop`, `%dsldocs` and also `%dsldf`, `%dslloopdf`,
* basic DSL language autocomplete enabled on magic commands (both query and docs) 


## v 0.5.5

* documentation of DSL updated to v1.19
* prototype autocomplete within jupyter magic commands
* methods total_count and errors_string to API result object


## v 0.5.4

* dataframe helper methods for grants: `as_dataframe_funders` and `as_dataframe_investigators`
* magic methods `%%dsl_query_as_df` returning a dataframe
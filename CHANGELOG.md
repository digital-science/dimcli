# Changelog

## v 0.6

* Query Warnings and Error messages printed out by default in Jupyter environments
* Added `verbose` option to suppress all messages (default = True)
  * `dsl = dimcli.Dls(verbose=False)`: global 
  * `dsl.query(q, verbose=False)`: local for a specific query
* Improved `query_iterative` to handle max 50k results and timeouts (from too many queries)
* Refactored REPL module and imports 


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
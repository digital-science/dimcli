# Changelog



## v 0.9.2

* CLI: `.record_notebook` utility removed. Use instead `.export_as_jupyter`
* Added support for new V2 API endpoints


## v 0.9.1

* DSL grammar updated for version 1.31 (2021-05 release)


## v 0.9

* DSL grammar updated for version 1.30 (2021-03 release)


## v 0.8.2

* CLI - new `export_gist` command to export query as a Github Gist
* Fix for `extract_affiliations` UTF-8 bug


## v 0.8.1

* Improve warning messages for deprecated modules 
* Add cumulative warnings to `Dsl.query_iterative` 
* Fix for dimcli CLI not showing records previews correctly 

## v 0.8

* Dimcli module level documentation vastly updated
  * See https://digital-science.github.io/dimcli/modules.html
* new `utils` module: misc utilities all grouped under `dimcli.utils`
  * `dimcli.shortcuts` is deprecated in favor of `dimcli.utils` 
  * the pyvis wrapper is now located at `dimcli.utils.networkviz`
* new magic commands: 
  * `%%dslgsheets` 
  * `%%dslloopgsheets`
  * `%%extract_concepts`
  * `%%identify_experts`
* new DSL functions Python wrappers: 
  * `extract_affiliations`
  * `identify_experts`
  * `build_reviewers_matrix`
* CLI - command line tool options improved
  * options `-w` for webapp search, `-i` for webapp object ID resolver
  

## v 0.7.5

* Gsheets export shortcuts
  * Export DSL results to gsheets: `DslDataset.to_gsheets()`
  * CLI command: `.export_as_gsheets`
  * `utils.export_as_gsheets` accepts both API JSON and (any) pd.DataFrame
* DSL grammar updated for version 1.28 (2020-09 release)
* Bug fix: json_normalize errors when creating 
* Updated DSL grammar for dimcli CLI autocomplete
* fix bug caused by new `_copyright` in JSON response 
* `to_json_file` replaces `DslDataset.save_json`


## v 0.7.4

* DSL grammar updated for version 1.27 (2020-08 release)
  * Refactoring of grammar objects 
* Added methods to save/load JSON data from DslDataset object
  * `DslDataset.load_json_file` (class method) and `DslDataset.save_json` (object method)
* `Dsl.query_iterative` takes an extra argument `maxlimit` forcing to stop the iteration when N results have been extracted


## v 0.7.3

* Improve support for iterative queries using DSL `unnest` operator 
* Time elapsed info

## v 0.7.2

* DSL grammar updated for version 1.26 (2020-07 release) 


## v 0.7.1

* refactored functions wrappers location `dimcli.core.functions.*` but can be imported using `dimcli.shortcurts` 


## v 0.7

* `DslDataset.as_dataframe_concepts()` method: refactoring so to handle latest concept scores
* `shortcuts.extract_concepts` method: wrapper for DSL function
* `shortcuts.extract_classification` method: wrapper for DSL function
* `shortcuts.extract_grants` method: wrapper for DSL function


## v 0.6.9

* improved login feedback message
* automated check for latest Dimcli version at login 
* `dimcli.DslDataset`  is the new name of dimcli.Dataset, to avoid conflicts with Dataset documents in Dimensions
* DSL grammar updated for version 1.25 (2020-05-28 release) 
* CLI: new command `export_as_jupyter`


## v 0.6.8

* DSL grammar updated for version 1.24 (2020-05-11 release)
* fix bug caused by new `_version` and `_notes` key in JSON response 
* support for key-based authentication methods


## v 0.6.7

* `df_grant_investigators_affiliations` new dataframe shortcut for grants results
* `dsl_escape` accepts boolean arg for escaping any special character (by default it escapes only `"`)
* `dsl.query_iterative` new argument: `force`: if any error if encountered during the extraction of a batch, it forces the iteration to continue
* CLI: pretty printing for `.json_compact` command


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
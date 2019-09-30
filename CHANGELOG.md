# Changelog


## v 0.5.8

* removed `json2html` dependency and simplified html export (from console)


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
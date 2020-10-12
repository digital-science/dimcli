Welcome to DimCli's documentation!
==================================

Dimcli is a Python client for accessing the Dimensions Analytics API. 

Dimcli lives on `Github <https://github.com/digital-science/dimcli/>`_. Suggestions, pull requests and improvements welcome!

.. code::

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



About Dimensions Analytics API
-------------------------------

The `Dimensions Analytics API <https://www.dimensions.ai/dimensions-apis/>`_ supports extraction of Dimensions data for use in complex analyses and visualizations or the building of analytical tools and reporting templates. The API uses an intuitive `query language <https://docs.dimensions.ai/dsl>`_ specifically developed for Dimensions data. You can retrieve, aggregate, and sort data from highly specific requests in a single API call. Additional services like text categorization are also available. 

Digital Science's `Dimensions <https://app.dimensions.ai/>`_ is a linked-research data platform that allows to explore the connections between more than 150 million records including grants, publications, clinical trials, patents and policy documents.

For more information about the Dimensions Analytics API, see also: 

* The `Dimensions API Lab <https://api-lab.dimensions.ai/>`_ , an open source collection of jupyter notebooks tutorials
* The official `Dimensions API Documentation <https://docs.dimensions.ai/dsl/>`_



.. toctree::
   :maxdepth: 3
   :caption: Contents

   getting-started
   modules




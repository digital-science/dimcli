Welcome to DimCli's documentation!
==================================

Dimcli is a Python client for accessing the `Dimensions Analytics API <https://www.dimensions.ai>`_. 

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



About Dimensions APIs
---------------------

Digital Science's `Dimensions <https://app.dimensions.ai/>`_ is a linked-research data platform that allows to explore the connections between millions of objects including grants, publications, clinical trials, patents and policy documents.

For more information about the Dimensions APIs, see: 

* the `Dimensions API Lab <https://api-lab.dimensions.ai/>`_ 
* the official `Dimensions API Documentation <https://docs.dimensions.ai/dsl/>`_



.. toctree::
   :maxdepth: 2
   :caption: Contents

   readme
   apidocs




"""
This module contains utilities for working with the API / data it returns.  

NOTE: these functions are attached to the top level ``dimcli.utils`` module. E.g.:

>>> from dimcli.utils import dimensions_url
>>> dimensions_url("pub.1127419018")
'https://app.dimensions.ai/details/publication/pub.1127419018'

"""

from .misc_utils import *
from .dim_utils import *
from .converters import *
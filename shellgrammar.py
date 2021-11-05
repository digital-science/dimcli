#
# startup file for ipython
#
# used to generate a new version of the grammar_dsl.py file 
#

import json
import dimcli
dimcli.login(instance="live")
dsl = dimcli.Dsl()

data = dsl.query("describe schema").json

with open("dimcli/core/dsl_grammar_core_NEW.py", "w") as f:
    f.write("GRAMMAR_DICT = " + str(data))


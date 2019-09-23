
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class

from ..VERSION import VERSION

from ..core.api import Dsl
from ..core.auth import get_connection, is_logged_in
from ..core.utils import *


@magics_class
class DslMagics(Magics):

    results_var = "dsl_last_results" # VAR AUTOMATICALLY SET TO LATEST QUERY RESULTS
    dslobject = None


    def _handle_login(self):
        if is_logged_in():
            self.dslobject = Dsl(show_results=False)
            return True
        else:
            return False


    def _handle_query(self, text, loop=False):
        """main procedure after user input"""
       
        # lazy complete
        text = line_add_lazy_return(text)
        text = line_add_lazy_describe(text)

        # RUN QUERY
        if not loop:
            res = self.dslobject.query(text)
        else:
            res = self.dslobject.query_iterative(text)
            return res
        
        # print results
        if "errors" in res.data.keys():
            if "query" in res.data["errors"]:
                print(res.data["errors"]["query"]["header"])
                for key in res.data["errors"]["query"]["details"]:
                    print(key)
            else:
                print(res.data["errors"])
        else:
            print_json_stats(res, text)
            return res


    #
    # MAGIC METHODS
    # 


    @line_cell_magic
    def dsl(self, line, cell=None):
        """
        DimCli Magic Method: enter a DSL query string and send it directly to Dimensions API. 
        """
        if self._handle_login():
            if cell:
                line = cell
            data = self._handle_query(line)
            self.shell.user_ns[self.results_var] = data
            return data


    @line_cell_magic
    def dsldf(self, line, cell=None):
        """DimCli Magic method: query the Dimensions DSL API with the text passed - return a pandas dataframe.
        """
        if self._handle_login():
            if cell:
                line = cell
            data = self._handle_query(line).as_dataframe()
            self.shell.user_ns[self.results_var] = data
            return data


    @line_cell_magic
    def dslloop(self, line, cell=None):
        """DimCli Magic Method: transforms a simple query into a loop, by adding limit/skip parameters automatically. The final object returns contains all results into a single JSON object.  
        """
        if self._handle_login():
            if cell:
                line = cell
            data = self._handle_query(line, loop=True)
            self.shell.user_ns[self.results_var] = data
            return data


    @line_cell_magic
    def dslloopdf(self, line, cell=None):
        """DimCli Magic method: query the Dimensions DSL API with the text passed, looping over all results pages - return a pandas dataframe.
        """
        if self._handle_login():
            if cell:
                line = cell
            data = self._handle_query(line, loop=True).as_dataframe()
            self.shell.user_ns[self.results_var] = data
            return data


    @line_magic
    def dsldocs(self, line):
        """
        DimCli Magic method: wrapper around the dsl `describe` function - outputs documentation for a DSL Source or Entity as a pandas dataframe.
        """
        if not self._handle_login():
            return

        try:
            import pandas as pd
            df = pd.DataFrame()
        except:
            print("Sorry this functionality requires the Pandas python library. Please install it first")
            return

        obj = line.strip()
        if obj and obj not in G.entities() and obj not in G.sources():
            sou = " - ".join([x for x in G.sources()])
            ent = " - ".join([x for x in G.entities()])
            print(f"Sorry can't recognize this object. Use one of the following: Sources=[{sou}] Entities=[{ent}] ")
            return
        
        res = self._handle_query(f"describe schema") # same query for all requests (filtering done here)

        if not obj:
            docs_for = G.sources()
            header = "sources"
        elif obj in G.entities():
            docs_for = [obj]
            header = "entities"
        elif obj in G.sources():
            docs_for = [obj]
            header = "sources"

        d = {header: [], 'field': [], 'type': [], 'description':[], 'is_filter':[], 'is_entity': [],  'is_facet':[],}
        for S in docs_for:
            for x in sorted(res.json[header][S]['fields']):
                d[header] += [S]
                d['field'] += [x]
                d['type'] += [res.json[header][S]['fields'][x]['type']]
                d['description'] += [res.json[header][S]['fields'][x]['description']]
                d['is_filter'] += [res.json[header][S]['fields'][x]['is_filter']]
                d['is_facet'] += [res.json[header][S]['fields'][x].get('is_facet', False)]
                d['is_entity'] += [res.json[header][S]['fields'][x].get('is_entity', False)]

        return df.from_dict(d)




    #
    # ===DEPRECATED==== MAGIC METHODS (from v 0.5.6)
    # 

    @line_magic
    def dsl_login(self, line):
        print("DEPRECATED Magic - please use `dimcli.login()` instead. ")
        print("""e.g. `import dimcli; dimcli.login(username="", password="", endpoint="https://app.dimensions.ai", instance="live")`""")

    @line_cell_magic
    def dsl_query(self, line, cell=None):
        print("DEPRECATED Magic - please use `%dsl` instead. ")

    @line_cell_magic
    def dsl_query_loop(self, line, cell=None):
        print("DEPRECATED Magic - please use `%dslloop` instead. ")

    @line_cell_magic
    def dsl_query_as_df(self, line, cell=None):
        print("DEPRECATED Magic - please use `%dsldf` instead. ")


    @line_cell_magic
    def dsl_query_loop_as_df(self, line, cell=None):
        print("DEPRECATED Magic - please use `%dslloopdf` instead. ")

    @line_magic
    def dsl_docs(self, line):
        print("DEPRECATED Magic - please use `%dsldocs` instead. ")






ip = get_ipython()
ip.register_magics(DslMagics)

from ..repl.autocompletion import CleverCompleter
from prompt_toolkit.document import Document

def load_ipython_custom_completers(ipython):
    """

    # TODO 
    # check more Completer behaviour in order to remove extra suggestions eg
    # https://www.programcreek.com/python/example/50972/IPython.get_ipython


    """

    def dslq_completers(self, event):
        """ This should return a list of strings with possible completions.

        Note that all the included strings that don't start with event.symbol
        are removed, in order to not confuse readline.

        eg Typing %%apt foo then hitting tab would yield an event like so: namespace(command='%%apt', line='%%apt foo', symbol='foo', text_until_cursor='%%apt foo')

        https://stackoverflow.com/questions/36479197/ipython-custom-tab-completion-for-user-magic-function

        > https://github.com/ipython/ipython/issues/11878
        """
        # print(dir(event), event)

        # FIXME only first line gets the autocomplete!
        if event.line.startswith("%%"):
            event.line = event.line[1:] #  reduce cell symbol (double %) to line symbol
        for command in ["%dslloopdf", "%dsldf", "%dslloop", "%dsl"]:
            if command in event.line: # first match will return results
                doc = Document(event.line.replace(command, ""))
                c = CleverCompleter()
                res = c.get_completions(doc, None)
                # print(res)
                return [x.text for x in res]
            
    def dsldocs_completers(self, event):
        """ 
        Completer for dsldocs command (= describe)
        """
        # print(dir(event), event)
        command = "%dsldocs"
        if event.line.startswith(command):
            doc = Document(event.line.replace(command, ".docs"))
            c = CleverCompleter()
            res = c.get_completions(doc, None)
            # print(res)
            return [x.text for x in res]           

    
    # loader

    for command in ["%dslloop_to_dataframe", "%dsl_to_dataframe", "%dslloop", "%dsl"]:
        ipython.set_hook('complete_command', dslq_completers, re_key = command)
        ipython.set_hook('complete_command', dslq_completers, re_key = "%" + command)

    ipython.set_hook('complete_command', dsldocs_completers, re_key = "%dsldocs")


load_ipython_custom_completers(ip)




# ****************************************************************************

# 
# MEMOS 
# 

# ARGUMENTS AND LINE MAGICS 
# 
# line magics and arguments don't play well together when you need to parse a line content
# in that case the args parsing throws an error
# hence better to have a cell magic, and pass only the args in the line

# @magic_arguments.magic_arguments()
# @magic_arguments.argument('--endpoint',
#     help='The query endpoint: default is https://app.dimensions.ai'
# )
# @magic_arguments.argument('--user',
#     help='The account username'
# )
# @magic_arguments.argument('--password',
#     help='The account password'
# )
# @magic_arguments.argument('--env',
#     help='The instance name as defined in init.py. Default: live.'
# )


# ****************************************************************************
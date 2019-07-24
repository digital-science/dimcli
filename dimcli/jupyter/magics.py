
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class

from ..VERSION import VERSION

from ..core.api import Dsl
from ..core.config import *
from ..core.utils import *


@magics_class
class DslMagics(Magics):

    results_var = "dsl_last_results" # VAR AUTOMATICALLY SET TO LATEST QUERY RESULTS

    
    # NOTE line magics and arguments don't play well together when you need to parse a line content
    # in that case the args parsing throws an error
    # hence better to have a cell magic, and pass only the args in the line

    @line_magic
    @magic_arguments.magic_arguments()
    @magic_arguments.argument('--endpoint',
      help='The query endpoint: default is https://app.dimensions.ai'
    )
    @magic_arguments.argument('--user',
      help='The account username'
    )
    @magic_arguments.argument('--password',
      help='The account password'
    )
    @magic_arguments.argument('--env',
      help='The instance name as defined in init.py. Default: live.'
    )
    def dsl_login(self, line):
        """DimCli Magic
        Authenticate with the Dimensions.ai DSL backend. If not args are passed, it assumed you have set up a dsl.ini file: see https://github.com/lambdamusic/dimcli#the-credentials-file).
        
        Alternatively one can pass auth details explicitly eg
        >>> %dsl_login --user=me@mail.com --password=secret

        """
        args = magic_arguments.parse_argstring(self.dsl_login, line)
        # print(args)
        usr = args.user
        psw = args.password
        endpoint = args.endpoint or "https://app.dimensions.ai"
        instance = args.env or "live"

        if usr and psw:
            self.dsl = Dsl(user=usr, password=psw, endpoint=endpoint, show_results=False, force_login=True)
            print("DimCli %s - Succesfully connected to <%s> (method: manual login)" % (str(VERSION), self.dsl._url)) 
        else:
            # try to use local init file using instance parameter
            self.dsl = Dsl(instance=instance, show_results=False, force_login=True) 
            print("DimCli %s - Succesfully connected to <%s> (method: dsl.ini file)" % (str(VERSION), self.dsl._url))


    @line_cell_magic
    def dsl_query(self, line, cell=None):
        """DimCli Magic
        Query the Dimensions DSL API with the text passed. 
        """
        if self._handle_login():
            if cell:
                line = cell
            data = self._handle_query(line)
            self.shell.user_ns[self.results_var] = data
            return data
            
        else:
            print("Please login first: %dsl_login")

    @line_cell_magic
    def dsl_query_loop(self, line, cell=None):
        """DimCli Magic
        Query the Dimensions DSL API with the text passed, looping over all results pages. The final object returns contains all results into a single JSON object.  
        """
        if self._handle_login():
            if cell:
                line = cell
            data = self._handle_query(line, loop=True)
            self.shell.user_ns[self.results_var] = data
            return data

        else:
            print("Please login first: %dsl_login")


    def _handle_login(self):
        if self.dsl: 
            return True
        else:
            if CONNECTION['token']:
                self.dsl = Dsl(show_results=False)
                return True
        return False


    def _handle_query(self, text, loop=False):
        """main procedure after user input"""
       
        # lazy complete
        text = line_add_lazy_return(text)
        text = line_add_lazy_describe(text)

        # RUN QUERY
        if not loop:
            res = self.dsl.query(text)
        else:
            res = self.dsl.query_iterative(text)
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


    @line_magic
    def dsl_docs(self, line):
        """DimCli Magic
        Wrapper around the dsl `describe` function - outputs live documentation for a source or entity
        """
        if not self.dsl:
            print("Please login first: %dsl_login")
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







ip = get_ipython()
ip.register_magics(DslMagics)



from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class

from ..VERSION import VERSION

from ..core.api import Dsl
from ..core.utils import *

@magics_class
class DslMagics(Magics):

    connection = None

    
    # @magic_arguments.magic_arguments()
    # @magic_arguments.argument('env', type="string",
    #       help='Which dimensions backend to use'
    # )
    @line_magic
    def dsl_login(self, line):
        """DimCli Magic
        Authenticate with the Dimensions.ai DSL backend. Requires a dsl.ini file (see https://github.com/lambdamusic/dimcli#the-credentials-file). 
        Accepts an argument matching the instance name in the credentials file (default=live)
        """
        instance = line.strip() or "live"
        self.connection = Dsl(instance=instance, show_results=False) 
        print("DimCli %s - Succesfully connected to <%s>" % (str(VERSION), self.connection._url))

    @line_cell_magic
    def dsl_query(self, line, cell=None):
        """DimCli Magic
        Query the Dimensions DSL API with the text passed. 
        """
        if self.connection:
            if cell:
                line = cell
            return self._handle_query(line)
            
        else:
            print("Please login first: %dsl_login")

    @line_cell_magic
    def dsl_query_loop(self, line, cell=None):
        """DimCli Magic
        Query the Dimensions DSL API with the text passed, looping over all results pages. The final object returns contains all results into a single JSON object.  
        """
        if self.connection:
            if cell:
                line = cell
            return self._handle_query(line, loop=True)
            # return self.connection.query_iterative(line)

        else:
            print("Please login first: %dsl_login")


    def _handle_query(self, text, loop=False):
        """main procedure after user input"""
       
        # lazy complete
        text = line_add_lazy_return(text)
        text = line_add_lazy_describe(text)

        # RUN QUERY
        if not loop:
            res = self.connection.query(text)
        else:
            res = self.connection.query_iterative(text)
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
            print_json_summary(res, text)
            return res


    @line_magic
    def dsl_schema(self, line):
        "Wrapper around the dsl describe function"
        if self.connection:
            return self._handle_query("describe schema")
        else:
            print("Please login first: %dsl_login")


ip = get_ipython()
ip.register_magics(DslMagics)


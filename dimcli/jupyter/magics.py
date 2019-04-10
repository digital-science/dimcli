
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class


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
        # args = magic_arguments.parse_argstring(self.hello, line)
        # if args.verbose:
        #     print('hello ' + cell)

        self.connection = Dsl(instance="live", show_results=False) 

    @line_cell_magic
    def dsl_query(self, line, cell=None):
        "Send a query to the DSL back end"
        if self.connection:
            if cell:
                line = cell
            return self._handle_query(line)
            
        else:
            print("Please login first: %dsl_login")

    @line_cell_magic
    def dsl_query_loop(self, line, cell=None):
        "Send an iterative query to the DSL back end"
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





ip = get_ipython()
ip.register_magics(DslMagics)


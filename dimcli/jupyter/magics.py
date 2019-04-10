
from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class


from ..core.api import Dsl
from ..repl.repl import handle_query

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
            return handle_query(self.connection, line, None)
            
        else:
            print("Please login first: %dsl_login")

    @line_cell_magic
    def dsl_loop(self, line, cell=None):
        "Send an iterative query to the DSL back end"
        if self.connection:
            if cell:
                line = cell
            return self.connection.query_iterative(line)

        else:
            print("Please login first: %dsl_login")




ip = get_ipython()
ip.register_magics(DslMagics)



from IPython.core import magic_arguments
from IPython.core.magic import line_magic, cell_magic, line_cell_magic, Magics, magics_class


from ..dimensions import Dsl
from ..repl.repl import handle_query

@magics_class
class DslMagics(Magics):

    CLIENT = None
    # @cell_magic
    # def hello(self, line='', cell=None):
    #     print('hello ' + cell)

    @line_magic
    def dsl_login(self, line):
        connection = Dsl(instance="live", show_results=False)
        self.CLIENT = connection 

    @line_magic
    def dsl(self, line):
        if self.CLIENT:
            return handle_query(self.CLIENT, line, None)
        else:
            print("Please login first: %dsl_login")
        # print('hi ' + line)

    @line_magic
    def dsl_loop(self, line):
        if self.CLIENT:
            return self.CLIENT.query_iterative(line)
        else:
            print("Please login first: %dsl_login")



ip = get_ipython()
ip.register_magics(DslMagics)
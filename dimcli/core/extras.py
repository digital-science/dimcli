"""
**DEPRECATED** 
NOTE This module is deprecated and will be removed in future versions.

Use instead `utils.networkviz`
"""

try:
    from pyvis.network import Network as PyvisNetwork
except ImportError:
    print("ERROR: this module requires pyvis `pip install pyvis`")
    raise

import IPython
import os
from .. import COLAB_ENV

print("WARNING: the `extras` module is deprecated. Use instead ``from dimcli.utils.networkviz import *``")


class NetworkViz(PyvisNetwork):
    """Extend PyVis class so that we can use a modified template. 

    Note: this is an experimental feature. 
    The modified template allows to display JS inline hence it works in Colab. 
    """
 
    def __init__(self,
                 height="500px",
                 width="500px",
                 directed=False,
                 notebook=False,
                 bgcolor="#ffffff",
                 font_color=False,
                 layout=None):
        # call super class init
        PyvisNetwork.__init__(self, 
                              height, 
                              width,
                              directed,
                              notebook,
                              bgcolor,
                              font_color,
                              layout)
        # override template location
        self.path =  os.path.abspath(os.path.join(os.path.dirname( __file__ ), '..', 'templates/pyvis_inline.html'))
        # self.path = os.path.dirname(__file__) + "/templates/pyvis_inline.html"

    def check_html(self, name):
        """
        Given a name of graph to save or write, check if it is of valid syntax

        :param: name: the name to check
        :type name: str
        """
        assert len(name.split(".")) >= 2, "invalid file type for %s" % name
        assert name.split(
            ".")[-1] == "html", "%s is not a valid html file" % name


    def show(self, name):
        """
        Writes a static HTML file and saves it locally before opening.

        :param: name: the name of the html file to save as
        :type name: str
        """
        self.check_html(name)
        if self.template is not None:
            if not COLAB_ENV: 
                # return IFrame(name, width=self.width, height=self.height)
                return self.write_html(name, notebook=True)
            else:
                self.write_html(name, notebook=True)
                return IPython.display.HTML(filename=name)
        else:
            self.write_html(name)
            webbrowser.open(name)
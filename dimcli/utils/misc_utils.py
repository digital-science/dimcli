"""
Dimcli general purpose utilities for working with data. 
NOTE: these functions are attached to the top level ``dimcli.utils`` module. So you can import them as follows:

>>> from dimcli.utils import *

"""



import click
import time
import json
import sys
import subprocess
import os
import re
import webbrowser
from itertools import islice

from pandas import DataFrame
try:
    from pandas import json_normalize
except:
    from pandas.io.json import json_normalize



def chunks_of(data, size):
    """Splits up a list or sequence in to chunks of selected size. 

    Parameters
    ----------
    data: sequence
        A sequence eg a list that needs to be chunked.
    size: int
        The number of items in each group.

    Returns
    -------
    Iterator
        An iterable

    Example
    -------
    >>> from dimcli.utils import chunks_of
    >>> a = range(10)
    >>> for x in chunks_of(a, 5):
            print(len(x))
    5
    5
    >>> list(chunks_of(a, 5))
    [[0, 1, 2, 3, 4], [5, 6, 7, 8, 9]]

    """
    it = iter(data)
    chunk = list(islice(it, size))
    while chunk:
        yield chunk
        chunk = list(islice(it, size))


def save2File(contents, filename, path):
    """Save string contents to a file, creating the file if it doesn't exist.

    NOTE Not generalized much, so use at your own risk.


    Parameters
    ----------
    contents: str
        File contents
    filename: str
        Name of the file.
    path: str
        Full path of the file to save. If not existing, it gets created.
    
    Returns
    -------
    str
        The file path with format  "file://..."

    """
    if not os.path.exists(path):
        os.makedirs(path)
    filename = os.path.join(path, filename)
    f = open(filename, 'wb')
    f.write(contents.encode())  # python will convert \n to os.linesep
    f.close()  # you can omit in most cases as the destructor will call it
    url = "file://" + filename
    return url





def open_multi_platform(fpath):
    """Open a file using the native OS tools, taking care of platform differences. 

    Supports win, macos and linux.
    """
    click.secho("Opening `%s` ..." % fpath)
    if sys.platform == 'win32':
        subprocess.Popen(['start', fpath], shell=True)

    elif sys.platform == 'darwin':
        subprocess.Popen(['open', fpath])

    else:
        try:
            subprocess.Popen(['xdg-open', fpath])
        except OSError:
            print("Couldnt find suitable opener for %s" % fpath)



def exists_key_in_dicts_list(dict_list, key):
    """From a list of dicts, checks if a certain key is in one of the dicts in the list.

    See also https://stackoverflow.com/questions/14790980/how-can-i-check-if-key-exists-in-list-of-dicts-in-python

    Parameters
    ----------
    dict_list: list 
        A list of dictionaries.
    key: obj 
        The obj to be found in dict keys

    Returns
    -------
    Dict or None

    """
    # return next((i for i,d in enumerate(dict_list) if key in d), None)
    return next((d for i,d in enumerate(dict_list) if key in d), None)



def normalize_key(key_name, dict_list, new_val=None):
    """Ensures the key always appear in a JSON dict/objects list by adding it when missing.

    UPDATE 2019-11-28
    v0.6.1.2: normalizes also 'None' values (to address 1.21 DSL change)

    Parameters
    ----------
    key_name : obj
        The dict key to normalize.
    dict_list : list
        List of dictionaries where to be processed.
    new_val : obj, optional
        Default value to add to the key, when not found. If `new_val` is not passed, it is inferred from first available non-empty value. 


    Returns
    -------
    dict
        Same dictionary being passed. Changes happen in-place.    

    Example
    -------------
    >>> for x in pubs_details.publications:
            if not 'FOR' in x:
                x['FOR'] = []

    becomes simply:
    
    >>> normalize_key("FOR", pubs_details.publications)

    """
    if new_val == None:
        for x in dict_list:
            if key_name in x:
                new_val = type(x[key_name])() # create empty object eg `list()`
                # print(new_val)
                break 
    for x in dict_list:
        if (not key_name in x) or (x[key_name] == None):
            x[key_name] = new_val




def export_as_gsheets(input_data, query="", title=None, verbose=True):
    """Save data to google sheets with one-line. 

    Works with raw JSON (from API), or even a Dataframe. 

    Parameters
    ----------
    input_data: JSON or DataFrame 
        The data to be uploaded
    query: str
        The DSL query - this is neeeded only when raw API JSON is passed
    title: str, optional 
        The spreadsheet title, if one wants to reuse an existing spreadsheet.
    verbose: bool, default=True
        Verbose mode

    Notes
    -----
    This method assumes that the calling environment can provide valid Google authentication credentials.
    There are two routes to make this work, depending on whether one is using Google Colab or a traditional Jupyter environment.

    **Google Colab**
    This is the easiest route. In Google Colab, all required libraries are already available. The `to_gsheets` method simply triggers the built-in authentication process via a pop up window. 
    
    **Jupyter**
    This route involves a few more steps. In Jupyter, it is necessary to install the ``gspread``, ``oauth2client`` and ``gspread_dataframe`` modules first. Secondly, one needs to create Google Drive access credentials using OAUTH (which boils down to a JSON file). Note that the credentials file needs to be saved in: `~/.config/gspread/credentials.json` (for gpread to work correctly). 
    These steps are described at https://gspread.readthedocs.io/en/latest/oauth2.html#for-end-users-using-oauth-client-id.

    Returns
    -------
    str
        The google sheet URL as a string.   

    Example
    -------
    >>> import pandas as pd
    >>> from dimcli.utils export_as_gsheets
    >>> cars = {'Brand': ['Honda Civic','Toyota Corolla','Ford Focus','Audi A4'],
                 'Price': [22000,25000,27000,35000]
                 }
    >>> df = pd.DataFrame(cars, columns = ['Brand', 'Price'])
    >>> export_as_gsheets(df)
    ..authorizing with google..
    ..creating a google sheet..
    ..uploading..
    Saved:
    https://docs.google.com/spreadsheets/d/1tsyRFDEsADltWDdqjuyDWDOg81sl9hN3Nu8MXVlqDDI
    """

    if 'google.colab' in sys.modules:
        from google.colab import auth
        auth.authenticate_user()

        import gspread
        from gspread_dataframe import set_with_dataframe
        from oauth2client.client import GoogleCredentials
        gc = gspread.authorize(GoogleCredentials.get_application_default())

    else:
        try:
            import gspread
            from oauth2client.service_account import ServiceAccountCredentials
            from gspread_dataframe import set_with_dataframe
        except:
            raise Exception("Missing libraries. Please install gspread, oauth2client and gspread_dataframe: `pip install gspread gspread_dataframe oauth2client -U`.")
        
        if verbose: click.secho("..authorizing with google..")
        try:
            gc = gspread.oauth()
        except:
            raise Exception("Google authorization failed. Do you have all the required files? Please see the documentation for more information: https://digital-science.github.io/dimcli/modules.html#dimcli.utils.misc_utils.export_as_gsheets")


    def line_search_return(line):
        """
        get the source/facet in the return statement
        Duplicates same method in dimcli.utils.repl_utils , to avoid circular imports
        """
        l = line.split()
        n = l.count("return")
        if n == 1:
            i = l.index("return")
            if len(l) > i + 1: # cause index is zero based
                return_obj = l[i + 1]
                if "[" in return_obj:
                    return return_obj.split('[')[0]
                else:
                    return return_obj
        else: # if multiple return values, fail
            return None

    if type(input_data) == type({}):
        # JSON
        if not query:
            raise Exception("When passing raw JSON you also have to provide the DSL query, which is needed to determine the primary records key.")            
        return_object = line_search_return(query)
        try:
            df =  json_normalize(input_data[return_object], errors="ignore")
        except:
            df =  json_normalize(input_data, errors="ignore")

    elif type(input_data) == DataFrame:
        # Dataframe
        df = input_data

    else:
        raise Exception(f"Input type '{str(type(input_data))}' not supported.")


    if title:
        if verbose: click.secho(f"..opening google sheet with title: {title}")
        gsheet = gc.open(title)  
    else:
        if verbose: click.secho("..creating a google sheet..")
        title = "dimcli-export-" + time.strftime("%Y%m%d-%H%M%S")
        gsheet = gc.create(title) 


    worksheet = gsheet.sheet1
    click.secho("..uploading..")
    set_with_dataframe(worksheet, df) 

    # https://gspread.readthedocs.io/en/latest/api.html#gspread.models.Spreadsheet.share
    gsheet.share(None, perm_type='anyone', role='reader') # anyone can see with url
    spreadsheet_url = "https://docs.google.com/spreadsheets/d/%s" % gsheet.id
    # if verbose: click.secho(f"Saved:\n{spreadsheet_url}", bold=True)
    return spreadsheet_url 




def google_url(stringa):
    """Generate a valid google search URL from a string (URL quoting is applied). 

    Example
    -------
    >>> from dimcli.utils import google_url
    >>> google_url("malaria AND africa")
    'https://www.google.com/search?q=malaria%20AND%20africa'
    """
    from urllib.parse import quote   
    s = quote(stringa)    
    return f"https://www.google.com/search?q={s}"
 





# https://gist.github.com/zdavkeos/1098474

def walk_up(bottom):
    """Mimic os.walk, but walk 'up' instead of down the directory tree

    Example
    -------
    #print all files and directories
    # directly above the current one
    >>> for i in walk_up(os.curdir):
    >>>    print(i)

    # look for a TAGS file above the
    # current directory
    >>> for c,d,f in walk_up(os.curdir):
    >>>    if 'TAGS' in f:
    >>>        print(c)
    >>>        break
    """

    bottom = os.path.realpath(bottom)

    #get files in current dir
    try:
        names = os.listdir(bottom)
    except Exception as e:
        print(e)
        return


    dirs, nondirs = [], []
    for name in names:
        if os.path.isdir(os.path.join(bottom, name)):
            dirs.append(name)
        else:
            nondirs.append(name)

    yield bottom, dirs, nondirs

    new_path = os.path.realpath(os.path.join(bottom, '..'))
    
    # see if we are at the top
    if new_path == bottom:
        return

    for x in walk_up(new_path):
        yield x



def printDebug(text, mystyle="", err=True, **kwargs):
    """Wrapper around click.secho() for printing in colors with various defaults.

    :kwargs = you can do printDebug("s", bold=True)

    2018-12-06: by default print to standard error stderr (err=True)
    https://click.palletsprojects.com/en/5.x/api/#click.echo
    This means that the output is ok with `less` and when piped to other commands (or files)

    Styling output:
    <http://click.pocoo.org/5/api/#click.style>
    Styles a text with ANSI styles and returns the new string. By default the styling is self contained which means that at the end of the string a reset code is issued. This can be prevented by passing reset=False.

    This works also with inner click styles eg

    ```python
    uri, title = "http://example.com", "My ontology"
    printDebug(click.style("[%d]" % 1, fg='blue') +
               click.style(uri + " ==> ", fg='black') +
               click.style(title, fg='red'))
    ```

    Or even with Colorama

    ```
    from colorama import Fore, Style

    printDebug(Fore.BLUE + Style.BRIGHT + "[%d]" % 1 + 
            Style.RESET_ALL + uri + " ==> " + Fore.RED + title + 
            Style.RESET_ALL)
    ```


    Examples:

    click.echo(click.style('Hello World!', fg='green'))
    click.echo(click.style('ATTENTION!', blink=True))
    click.echo(click.style('Some things', reverse=True, fg='cyan'))
    Supported color names:

    black (might be a gray)
    red
    green
    yellow (might be an orange)
    blue
    magenta
    cyan
    white (might be light gray)
    reset (reset the color code only)
    New in version 2.0.

    Parameters:
    text – the string to style with ansi codes.
    fg – if provided this will become the foreground color.
    bg – if provided this will become the background color.
    bold – if provided this will enable or disable bold mode.
    dim – if provided this will enable or disable dim mode. This is badly supported.
    underline – if provided this will enable or disable underline.
    blink – if provided this will enable or disable blinking.
    reverse – if provided this will enable or disable inverse rendering (foreground becomes background and the other way round).
    reset – by default a reset-all code is added at the end of the string which means that styles do not carry over. This can be disabled to compose styles.

    """

    if mystyle == "comment":
        click.secho(text, dim=True, err=err)
    elif mystyle == "important":
        click.secho(text, bold=True, err=err)
    elif mystyle == "normal":
        click.secho(text, reset=True, err=err)
    elif mystyle == "red" or mystyle == "error":
        click.secho(text, fg='red', err=err)
    elif mystyle == "green":
        click.secho(text, fg='green', err=err)
    else:
        click.secho(text, err=err, **kwargs)




def printInfo(text, mystyle="", **kwargs):
    """Wrapper around printDebug for printing ALWAYS to stdout
    This means that the output can be grepped etc..
    NOTE this output will be picked up by pipes etc..

    Fixes https://github.com/lambdamusic/Ontospy/issues/76
    """
    printDebug(text, mystyle, False, **kwargs)



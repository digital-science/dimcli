"""
This module contains various general purpose utilities.

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
from pandas import json_normalize, DataFrame



def chunks_of(data, size):
    """Splits up a list or sequence in to chunks of selected size. 

    Args:
        data: A sequence eg a list
        size: A number

    Returns:
        An iterable
    """
    it = iter(data)
    chunk = list(islice(it, size))
    while chunk:
        yield chunk
        chunk = list(islice(it, size))


def save2File(contents, filename, path):
    """Save string contents to a file.

    Not generalized much, so use at your own risk.

    Args:
        contents: string
        filename: string
        path: full valid path

    Returns:
        File location in URL format eg "file://..."
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
    """
    util to open a file on any platform (i hope)
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

    Args:
        dict_list: A list of dictionaries
        key: a string to be found in dict keys

    Returns:
        Dictionary or None
    """
    # return next((i for i,d in enumerate(dict_list) if key in d), None)
    return next((d for i,d in enumerate(dict_list) if key in d), None)



def normalize_key(key_name, dict_list, new_val=None):
    """Ensures the key always appear in a JSON dict/objects list, by adding it when missing 
    
    EG
    ```
    for x in pubs_details.publications:
        if not 'FOR' in x:
            x['FOR'] = []
    ```
    becomes
    
    ```
    normalize_key("FOR", pubs_details.publications)
    ```
    Changes happen in-place.

    TIP If `new_val` is not passed, it is inferred from first available non-empty value

    TODO add third argument to pass a lambda function for modifying key
    UPDATE 2019-11-28
    v0.6.1.2: normalizes also 'None' values (to address 1.21 DSL change)
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
    """Quick method to save some data to google sheets.

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
    This route involves a few more steps. In Jupyter, it is necessary to install the gspread, oauth2client and gspread_dataframe modules first. Secondly, one needs to create Google Drive access credentials using OAUTH (which boils down to a JSON file). Note that the credentials file needs to be saved in: `~/.config/gspread/credentials.json` (for gpread). 
    The steps are described at https://gspread.readthedocs.io/en/latest/oauth2.html#for-end-users-using-oauth-client-id.

    Returns
    -------
    str
        The google sheet URL as a string.   
        
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
            raise Exception("Google authorization failed. Do you have all the required files? Please see the documentation for more information.")


    if type(input_data) == type({}):
        # JSON
        if not query:
            raise Exception("When passing raw JSON you also have to provide the DSL query, which is needed to determine the primary records key.")            
        return_object = line_search_return(query)
        try:
            df =  json_normalize(jjson[return_object], errors="ignore")
        except:
            df =  json_normalize(jjson, errors="ignore")

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
    if verbose: click.secho(f"Saved:\n{spreadsheet_url}", bold=True)
    return spreadsheet_url 




def google_url(stringa):
    """
    Generate a valid google search URL from a string (URL quoting is applied)
    """
    from urllib.parse import quote   
    s = quote(stringa)    
    return f"https://www.google.com/search?q={s}"
 






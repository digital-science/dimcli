import requests
import click





class DimensionsClient(object):
    """
    Base class.
    Args:
        *args (list): list of arguments
        **kwargs (dict): dict of keyword arguments
    Attributes:
        self
    """
    _redirect_url = 'https://scigraph.springernature.com/api/redirect'
    _default_headers = {'Accept': 'application/rdf+xml'}

    def __init__(self, *args, **kwargs):
        allowed_keys = ['verbose']
        self.__dict__.update((k, False) for k in allowed_keys)
        self.__dict__.update((k, v) for k, v in kwargs.items() if k in allowed_keys)
        self.response = None

        self.entity = None

    # def get_response_from_id(self, **kwargs):
    #     """
    #     Function.#TODO
    #     """
    #     allowed_keys = ['uri', 'doi', 'issn', 'isbn']
    #     for k, v in kwargs.items():
    #         if k in allowed_keys:
    #             payload = {k: v}
    #             self.response = self._do_request(payload)
    #             return self.response
    #     if self.verbose: click.secho("Valid arguments: " + str(allowed_keys), fg="green")
    #     return None

    # def get_entity_from_id(self, **kwargs):
    #     """
    #     Function.#TODO
    #     """
    #     self.get_response_from_id(**kwargs)
    #     if self.response:
    #         rdf_url, rdf_text = self.response.url, self.response.text
    #         x = ontospy.Ontospy()
    #         if self.verbose: click.secho("... loading graph", fg="green")
    #         x.load_rdf(text=rdf_text)
    #         click.secho("Parsing %d triples.." % x.triplesCount(), fg="green")
    #         if self.verbose: click.secho("... building entity...", fg="green")
    #         # build SG Entity
    #         self.entity = x.build_entity_from_uri(rdf_url, SciGraphRdfEntity)
    #         return self.entity
    #     else:
    #         return None

    # def _do_request(self, payload, headers=None):
    #     """
    #     Function.#TODO
    #     """
    #     if not headers:
    #         headers = self._default_headers
    #     if 'uri' in payload:
    #         url = payload['uri']
    #         payload = {}
    #     else:
    #         url = self._redirect_url
    #     if self.verbose: click.secho("... requesting rdf", fg="green")
        
    #     r = requests.get(url, headers=headers, params=payload)
        
    #     if r.status_code == 404:
    #         return False
    #     else:
    #         if r.url.startswith("https://"):
    #             # https ok for retrieval, but rdf payload always uses http uris
    #             r.url = r.url.replace("https://", "http://")
    #         if self.verbose: click.secho("Found " + r.url, fg="green")
    #         return r



    # def print_report(self):
    #     if self.entity and self.response:
    #         # extract values
    #         label = self.entity.bestLabel() or "N/A"
    #         title = self.entity.title or "N/A"
    #         doi = self.entity.doi or "N/A"
    #         types = " ".join([x for x in self.entity.rdftype_qname])
    #         rdf_url, rdf_text = self.response.url, self.response.text
    #         # print
    #         click.echo(click.style('URI: ', fg='green') + click.style(' ' + rdf_url, reset=True))
    #         click.echo(click.style('DOI: ', fg='green') + click.style(' ' + doi, reset=True))
    #         click.echo(click.style('Label: ', fg='green') + click.style(' ' + label, reset=True))
    #         click.echo(click.style('Title: ', fg='green') + click.style(' ' + title, reset=True))
    #         click.echo(click.style('Types: ', fg='green') + click.style(' ' + types, reset=True))






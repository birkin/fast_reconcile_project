# -*- coding: utf-8 -*-

"""
Refactored version of original searcher.py
"""

import logging
import urllib.parse
from operator import itemgetter

import requests
from fast_reconcile_app import settings_app
from fast_reconcile_app.lib import text
from fuzzywuzzy import fuzz


log = logging.getLogger(__name__)


class Searcher( object ):

    def __init__( self ):
        self.api_base_url = settings_app.API_BASE_URL       # the OCLC fast-suggest-service
        self.fast_uri_base = settings_app.FAST_URI_BASE     # the worldcat.org fast-id-url
        self.default_query = settings_app.API_DEFAULT_QUERY
        self.refine_to_fast = self.prep_api_query_options()

    def prep_api_query_options( self ):
        """ Adds default_query to options-list.
            Called by __init__() """
        options = settings_app.API_QUERY_OPTIONS
        options.append( self.default_query )
        log.debug( 'options, ```%s```' % options )
        return options

    def search(self, raw_query, query_type='/fast/all'):
        """
        Hit the FAST API for names.
        """
        out = []
        unique_fast_ids = []
        query = text.normalize(raw_query).replace('the university of', 'university of').strip()
        query_type_meta = [i for i in self.refine_to_fast if i['id'] == query_type]
        if query_type_meta == []:
            query_type_meta = default_query
        query_index = query_type_meta[0]['index']
        try:
            #FAST api requires spaces to be encoded as %20 rather than +
            url = self.api_base_url + '?query=' + urllib.parse.quote(query)
            url += '&rows=30&queryReturn=suggestall%2Cidroot%2Cauth%2cscore&suggest=autoSubject'
            url += '&queryIndex=' + query_index + '&wt=json'
            log.debug( 'FAST API url is, ```%s``` ' % url )
            # app.logger.debug("FAST API url is " + url)
            resp = requests.get(url)
            results = resp.json()
        except Exception as e:
            log.warning( 'trouble hitting oclc, ```%s```' % e )
            # app.logger.warning(e)
            return out
        for position, item in enumerate(results['response']['docs']):
            match = False
            name = item.get('auth')
            alternate = item.get('suggestall')
            if (len(alternate) > 0):
                alt = alternate[0]
            else:
                alt = ''
            fid = item.get('idroot')
            fast_uri = self.make_uri(fid)
            #The FAST service returns many duplicates.  Avoid returning many of the
            #same result
            if fid in unique_fast_ids:
                continue
            else:
                unique_fast_ids.append(fid)
            score_1 = fuzz.token_sort_ratio(query, name)
            score_2 = fuzz.token_sort_ratio(query, alt)
            #Return a maximum score
            score = max(score_1, score_2)
            if query == text.normalize(name):
                match = True
            elif query == text.normalize(alt):
                match = True
            resource = {
                "id": fast_uri,
                "name": name,
                "score": score,
                "match": match,
                "type": query_type_meta
            }
            out.append(resource)
        #Sort this list by score
        sorted_out = sorted(out, key=itemgetter('score'), reverse=True)
        #Refine only will handle top three matches.
        return sorted_out[:3]
        ## end search()

    def make_uri( self, fast_id ):
        """
        Prepare a FAST url from the ID returned by the API.
        """
        fid = fast_id.lstrip('fst').lstrip('0')
        fast_uri = self.fast_uri_base.format(fid)
        return fast_uri

    ## end class Search()

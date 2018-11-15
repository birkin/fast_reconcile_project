# -*- coding: utf-8 -*-

import logging
import urllib.parse

import requests
from fast_reconcile_app.lib import text


log = logging.getLogger(__name__)


api_base_url = 'https://fast.oclc.org/searchfast/fastsuggest'

#Map the FAST query indexes to service types
default_query = {
    "id": "/fast/all",
    "name": "All FAST terms",
    "index": "suggestall"
}

refine_to_fast = [
    {
        "id": "/fast/geographic",
        "name": "Geographic Name",
        "index": "suggest51"
    },
    {
        "id": "/fast/corporate-name",
        "name": "Corporate Name",
        "index": "suggest10"
    },
    {
        "id": "/fast/personal-name",
        "name": "Personal Name",
        "index": "suggest00"
    },
    {
        "id": "/fast/event",
        "name": "Event",
        "index": "suggest11"
    },
    {
        "id": "/fast/title",
        "name": "Uniform Title",
        "index": "suggest30"
    },
    {
        "id": "/fast/topical",
        "name": "Topical",
        "index": "suggest50"
    },
    {
        "id": "/fast/form",
        "name": "Form",
        "index": "suggest55"
    }
]
refine_to_fast.append(default_query)


def search(raw_query, query_type='/fast/all'):
    """
    Hit the FAST API for names.
    """
    out = []
    unique_fast_ids = []
    query = text.normalize(raw_query).replace('the university of', 'university of').strip()
    query_type_meta = [i for i in refine_to_fast if i['id'] == query_type]
    if query_type_meta == []:
        query_type_meta = default_query
    query_index = query_type_meta[0]['index']
    try:
        #FAST api requires spaces to be encoded as %20 rather than +
        url = api_base_url + '?query=' + urllib.parse.quote(query)
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
        fast_uri = make_uri(fid)
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

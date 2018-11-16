# -*- coding: utf-8 -*-

import json, logging


log = logging.getLogger(__name__)


def parse_query( request ):
    """ Preps and returns three data-elements.
        Called by views.reconcile_v2() """
    ( query, query_type, callback ) = ( request.POST.get('query', None), request.POST.get('query_type', None), request.POST.get('callback', None) )
    if not query:
        query = request.GET.get( 'query', None )
    if query.startswith( '{' ):
        query = json.loads(query)['query']
    if not query_type:
        query_type = request.GET.get( 'query_type', '/fast/all' )
    if not callback:
        callback = request.GET.get( 'callback', None )
    log.debug( 'query, ```%s```; query_type, ```%s```; callback, ```%s```' % (query, query_type, callback) )
    return ( query, query_type, callback )

# -*- coding: utf-8 -*-

import json, logging


log = logging.getLogger(__name__)


def parse_query( request ):
    """ Preps and returns three data-elements.
        Called by views.reconcile_v2() """
    ( query, query_type, callback ) = ( request.POST.get('query', None), request.POST.get('query_type', None), request.POST.get('callback', None) )
    if not query:
        query = request.GET.get( 'query', None )
    query = massage_query( query )
    if not query_type:
        query_type = request.GET.get( 'query_type', '/fast/all' )
    if not callback:
        callback = request.GET.get( 'callback', None )
    log.debug( 'query, ```%s```; query_type, ```%s```; callback, ```%s```' % (query, query_type, callback) )
    return ( query, query_type, callback )


def massage_query( query ):
    """ Updates query for better fast-lookups.
        Called by parse_query() """
    if query.startswith( '{' ):
        query = json.loads(query)['query']
    elif '(' in query and ')' in query:
        substring = query[ query.find('(')+1:query.find(')') ]
        log.debug( 'substring, `%s`' % substring )
        wordcount = len( substring.split() )
        if wordcount > 1:
            query = query.replace( '(', '' )
            query = query.replace( ')', '' )
    log.debug( 'massaged query, `%s`' % query )
    return query

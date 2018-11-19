# -*- coding: utf-8 -*-

import datetime, json, logging, os, pprint

# from fast_reconcile_app.lib.shib_auth import shib_login  # decorator
from . import settings_app
from django.conf import settings as project_settings
from django.contrib.auth import logout
from django.core.urlresolvers import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from fast_reconcile_app.lib import query_parser, view_info_helper
from fast_reconcile_app.lib import searcher
from fast_reconcile_app.lib.misc import jsonpify
from fast_reconcile_app.lib.search import Searcher
from fast_reconcile_app.lib.searcher import search


log = logging.getLogger(__name__)

srchr = Searcher()


def info( request ):
    """ Returns basic data including branch & commit. """
    # log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    rq_now = datetime.datetime.now()
    commit = view_info_helper.get_commit()
    branch = view_info_helper.get_branch()
    info_txt = commit.replace( 'commit', branch )
    resp_now = datetime.datetime.now()
    taken = resp_now - rq_now
    context_dct = view_info_helper.make_context( request, rq_now, info_txt, taken )
    output = json.dumps( context_dct, sort_keys=True, indent=2 )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def reconcile_v1( request ):
    """ Performs oclc-lookup and massaging.
        Goal, to match response of original flask/python2 app as used by staff. """
    log.debug( 'request.__dict__, ```%s```' % request.__dict__ )
    ## single query
    ( query, query_type, callback ) = ( request.POST.get('query', None), request.POST.get('query_type', None), request.POST.get('callback', None) )
    if not query:
        query = request.GET.get( 'query', None )
    if not query_type:
        if query:
            query_type = request.GET.get( 'query_type', '/fast/all' )
        else:
            query_type = request.GET.get( 'query_type', None )
    if not callback:
        callback = request.GET.get( 'callback', None )
    log.debug( 'query, ```%s```; query_type, ```%s```; callback, ```%s```' % (query, query_type, callback) )
    if not query and not query_type:
        output = jsonpify( searcher.metadata, callback )
        return HttpResponse( output, content_type='application/json; charset=utf-8' )
        # return HttpResponse( 'no query' )
    if query.startswith( '{' ):
        query = json.loads(query)['query']
    results = search(query, query_type=query_type)
    # return jsonpify( {"result": results}, callback )
    output = jsonpify( {"result": results}, callback )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


def reconcile_v2( request ):
    """ Performs oclc-lookup and massaging requested by staff.
        Offers web-debug mode to see more of what's going on under-the-hood. """
    log.debug( 'request.__dict__, ```%s```' % pprint.pformat(request.__dict__) )
    ( query, query_type, callback ) = query_parser.parse_query( request )

    #If no type is specified this is likely to be the initial query
    #so lets return the service metadata so users can choose what
    #FAST index to use.
    if query is None and query_type is None:
        return jsonpify( settings_app.METADATA )


    results = srchr.search( raw_query=query, query_type=query_type )
    output = jsonpify( {"result": results}, callback )
    return HttpResponse( output, content_type='application/json; charset=utf-8' )


# @shib_login
# def login( request ):
#     """ Handles authNZ, & redirects to admin.
#         Called by click on login or admin link. """
#     next_url = request.GET.get( 'next', None )
#     if not next_url:
#         redirect_url = reverse( settings_app.POST_LOGIN_ADMIN_REVERSE_URL )
#     else:
#         redirect_url = request.GET['next']  # will often be same page
#     log.debug( 'redirect_url, ```%s```' % redirect_url )
#     return HttpResponseRedirect( redirect_url )

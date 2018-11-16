# -*- coding: utf-8 -*-

import logging
from django.test import TestCase
from fast_reconcile_app.lib import query_parser


log = logging.getLogger(__name__)

TestCase.maxDiff = None


class RootUrlTest( TestCase ):
    """ Checks root urls. """

    def test_root_url_no_slash(self):
        """ Checks '/root_url'. """
        response = self.client.get( '' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    def test_root_url_slash(self):
        """ Checks '/root_url/'. """
        response = self.client.get( '/' )  # project root part of url is assumed
        self.assertEqual( 302, response.status_code )  # permanent redirect
        redirect_url = response._headers['location'][1]
        self.assertEqual(  '/info/', redirect_url )

    ## end class RootUrlTest()


class QueryParserTest( TestCase ):
    """ Checks aspects of the perceived query. """

    def test_static_query(self):
        """ Checks basic queries that should not be changed. """
        self.assertEqual(
            'feminism',
            query_parser.massage_query( 'feminism' )
            )
        self.assertEqual(
            'Particles (physics)',
            query_parser.massage_query( 'Particles (physics)' )
            )

    def test_massaged_query(self):
        """ Checks queries that should be transformed. """
        self.assertEqual(
            'Particles Nuclear physics charm',
            query_parser.massage_query( 'Particles (Nuclear physics)' )
            )
        self.assertEqual(
            'zParticles (Nuclear physics charm)',
            query_parser.massage_query( 'Particles (Nuclear physics charm)' )
            )

    ## end class QueryParserTest()

# -*- coding: utf-8 -*-

import json


def jsonpify( data, callback ):
    """
    Helper to support JSONP
    """
    try:
        output = json.dumps( data, sort_keys=True, indent=2 )
        if callback:
            output = '%s(%s)' % ( callback, output )
        return output
    except Exception as e:
        message = 'exception jsonifying output, ```%s```' % e
        log.error( message )
        raise Exception( message )

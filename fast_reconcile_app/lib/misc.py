# -*- coding: utf-8 -*-

import json


def jsonpify( data, callback ):
    """
    Helper to support JSONP
    """
    try:
        if callback:
            output = '%s(%s)' % ( callback, json.dumps(data) )
        else:
            output = json.dumps( data )
        return output
    except Exception as e:
        message = 'exception jsonifying output, ```%s```' % e
        log.error( message )
        raise Exception( message )

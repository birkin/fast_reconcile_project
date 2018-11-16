# -*- coding: utf-8 -*-

import json, os


README_URL = os.environ['FST_RCNCL__README_URL']


##############################
# search.py
##############################

API_BASE_URL = 'https://fast.oclc.org/searchfast/fastsuggest'

FAST_URI_BASE = 'http://id.worldcat.org/fast/{0}'

API_DEFAULT_QUERY = {
    "id": "/fast/all",
    "name": "All FAST terms",
    "index": "suggestall"
}

API_QUERY_OPTIONS = [
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


## auth
# SUPER_USERS = json.loads( os.environ['FST_RCNCL__UPER_USERS_JSON'] )
# STAFF_USERS = json.loads( os.environ['FST_RCNCL__STAFF_USERS_JSON'] )  # users permitted access to admin
# STAFF_GROUP = os.environ['FST_RCNCL__STAFF_GROUP']  # not grouper-group; rather, name of django-admin group for permissions
# TEST_META_DCT = json.loads( os.environ['FST_RCNCL__TEST_META_DCT_JSON'] )
# POST_LOGIN_ADMIN_REVERSE_URL = os.environ['FST_RCNCL__POST_LOGIN_ADMIN_REVERSE_URL']  # tricky; for a direct-view of a model, the string would be in the form of: `admin:APP-NAME_MODEL-NAME_changelist`

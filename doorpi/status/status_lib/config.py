#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

def get(*args, **kwargs):
    try:
        if not kwargs.get('name'):
            kwargs['name'] = ['']
        if not kwargs.get('value'):
            kwargs['value'] = ['']
        return_dict = {}
        for section_request in kwargs['name']:
            for section in kwargs['DoorPiObject'].config.get_sections(section_request):
                return_dict[section] = {}
                for value_request in kwargs['value']:
                    for key in kwargs['DoorPiObject'].config.get_keys(section, value_request):
                        return_dict[section][key] = kwargs['DoorPiObject'].config.get(section, key)

        return {k: v for k, v in return_dict.items() if v}
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create '+str(__name__)+' object - '+str(exp)}

def is_active(doorpi_object):
    return bool(doorpi_object.config)

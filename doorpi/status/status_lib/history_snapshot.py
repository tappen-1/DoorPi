#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
import os
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

DOORPI_SECTION = 'DoorPi'

def get(*args, **kwargs):
    files = dict()
    try:
        if not kwargs.get('name'):
            kwargs['name'] = ['']
        if not kwargs.get('value'):
            kwargs['value'] = ['']

        path = kwargs['DoorPiObject'].config.get_string_parsed(DOORPI_SECTION, 'snapshot_path')
        if os.path.exists(path):
            files = [os.path.join(path, i) for i in os.listdir(path)]
            files = sorted(files, key=os.path.getmtime)
            if 'DoorPiWeb' in path:
                changedpath = path[path.find('DoorPiWeb')+len('DoorPiWeb'):]
                files = [f.replace(path, changedpath) for f in files]
        return files
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create '+str(__name__)+' object - '+str(exp)}

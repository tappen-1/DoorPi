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

        event_handler = kwargs['DoorPiObject'].event_handler

        status = {}
        for name_requested in kwargs['name']:
            if name_requested == 'sources':
                status['sources'] = event_handler.sources
            if name_requested == 'events':
                status['events'] = event_handler.events
            if name_requested == 'events_by_source':
                status['events_by_source'] = event_handler.events_by_source
            if name_requested == 'actions':
                status['actions'] = {event: [str(action) for action in event_handler.actions[event]] for event in event_handler.actions}
            if name_requested == 'threads':
                status['threads'] = str(event_handler.threads)
            if name_requested == 'idle':
                status['idle'] = event_handler.idle

        return status
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create '+str(__name__)+' object - '+str(exp)}

def is_active(doorpi_object):
    return bool(doorpi_object.event_handler)

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

        keyboard = kwargs['DoorPiObject'].keyboard

        status = {}

        for name_requested in kwargs['name']:
            if name_requested == 'name':
                status['name'] = keyboard.name

            if name_requested == 'input':
                status['input'] = {}
                for value_requested in kwargs['value']:
                    for input_pin in keyboard.input_pins:
                        if value_requested in input_pin:
                            status['input'][input_pin] = keyboard.status_input(input_pin)

            if name_requested == 'output':
                status['output'] = keyboard.output_status
                for value_requested in kwargs['value']:
                    status['output'] = {output_pin: value for output_pin, value in status['output'].items() if value_requested in output_pin}

        return status

    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create keyboard object - '+str(exp)}

def is_active(doorpi_object):
    try:
        return bool(doorpi_object.keyboard.name)
    except:
        return False

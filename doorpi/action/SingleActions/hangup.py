#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

import doorpi
from doorpi.action.base import SingleAction
from time import sleep

def hangup(waittime):
    logger.trace("hangup requested")
    if waittime > 0:
        logger.debug(f"Waiting {waittime} seconds before sending hangup request")
        sleep(float(waittime))
    return doorpi.DoorPi().sipphone.hangup()

def get(parameters):
    if not parameters.isdigit():
        return None
    return HangupAction(hangup, parameters)

class HangupAction(SingleAction):
    pass

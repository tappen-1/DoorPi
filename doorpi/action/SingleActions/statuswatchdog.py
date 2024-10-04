#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

from doorpi.action.base import SingleAction
import doorpi

def write_status_watchdog(watchdog_path, timeout):
    timeout = int(timeout)

    try:
        with open(watchdog_path, "w+") as watchdog:
            watchdog.write('\n')
            watchdog.flush()
    except Exception as e:
        logger.warning(f"while action write_status_watchdog - error opening watchdog file: {e}")
        return False

    return True

def get(parameters):
    parameter_list = parameters.split(',')
    if len(parameter_list) not in [1, 2]:
        return None

    watchdog = parameter_list[0]
    timeout = 5

    if len(parameter_list) == 2:
        timeout = int(parameter_list[1])

    return SleepAction(write_status_watchdog, watchdog, timeout)

class SleepAction(SingleAction):
    pass

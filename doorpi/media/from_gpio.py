#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class GpioKeyboard:
    def __init__(self):
        logger.debug("GpioKeyboard initialized")

    def destroy(self):
        logger.debug("Destroy GpioKeyboard")

    @staticmethod
    def load():
        return GpioKeyboard()

    @staticmethod
    def unload():
        logger.debug("Unload GpioKeyboard")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class Pn532Keyboard:
    def __init__(self):
        logger.debug("Pn532Keyboard initialized")

    def destroy(self):
        logger.debug("Destroy Pn532Keyboard")

    @staticmethod
    def load():
        return Pn532Keyboard()

    @staticmethod
    def unload():
        logger.debug("Unload Pn532Keyboard")

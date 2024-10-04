#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class Rdm6300Keyboard:
    def __init__(self):
        logger.debug("Rdm6300Keyboard initialized")

    def destroy(self):
        logger.debug("Destroy Rdm6300Keyboard")

    @staticmethod
    def load():
        return Rdm6300Keyboard()

    @staticmethod
    def unload():
        logger.debug("Unload Rdm6300Keyboard")

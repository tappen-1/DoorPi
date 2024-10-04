#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class DummyKeyboard:
    def __init__(self):
        logger.debug("DummyKeyboard initialized")

    def destroy(self):
        logger.debug("Destroy DummyKeyboard")

    @staticmethod
    def load():
        return DummyKeyboard()

    @staticmethod
    def unload():
        logger.debug("Unload DummyKeyboard")

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class FilesystemKeyboard:
    def __init__(self):
        logger.debug("FilesystemKeyboard initialized")

    def destroy(self):
        logger.debug("Destroy FilesystemKeyboard")

    @staticmethod
    def load():
        return FilesystemKeyboard()

    @staticmethod
    def unload():
        logger.debug("Unload FilesystemKeyboard")

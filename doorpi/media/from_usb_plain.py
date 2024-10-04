#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import logging
import doorpi

logger = logging.getLogger(__name__)

class UsbPlainKeyboard:
    def __init__(self):
        logger.debug("UsbPlainKeyboard initialized")

    def destroy(self):
        logger.debug("Destroy UsbPlainKeyboard")

    @staticmethod
    def load():
        return UsbPlainKeyboard()

    @staticmethod
    def unload():
        logger.debug("Unload UsbPlainKeyboard")

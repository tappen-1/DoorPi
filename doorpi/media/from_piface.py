#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class PifaceKeyboard:
    def __init__(self):
        logger.debug("PifaceKeyboard initialized")

    def destroy(self):
        logger.debug("Destroy PifaceKeyboard")

    @staticmethod
    def load():
        return PifaceKeyboard()

    @staticmethod
    def unload():
        logger.debug("Unload PifaceKeyboard")

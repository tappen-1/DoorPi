#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class KeyboardAbstractBaseClass:
    @staticmethod
    def load():
        logger.debug("KeyboardAbstractBaseClass loaded")
        return None

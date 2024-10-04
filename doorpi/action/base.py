#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class SingleAction:
    def __init__(self, action):
        self.action = action
        logger.debug(f"SingleAction initialized with action {self.action}")

    def execute(self):
        try:
            logger.debug(f"Executing action: {self.action}")
            self.action()
        except Exception as e:
            logger.error(f"Failed to execute action: {e}")

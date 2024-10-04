#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

try:
    import linphone
except ImportError:
    logger.warning("Linphone is not installed. Please install it to use this SIPPhone interface")

class Sipphone:
    def __init__(self):
        logger.info("Linphone SIPPhone initialized")

    def start(self):
        logger.info("Linphone SIPPhone started")

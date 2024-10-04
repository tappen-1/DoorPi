#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

try:
    import pjsua as pj
except ImportError:
    logger.warning("Pjsua is not installed. Please install it to use this SIPPhone interface")

class Sipphone:
    def __init__(self):
        logger.info("Pjsua SIPPhone initialized")

    def start(self):
        logger.info("Pjsua SIPPhone started")

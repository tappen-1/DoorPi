#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)

class Sipphone:
    def __init__(self):
        logger.info("Dummy SIPPhone initialized")

    def start(self):
        logger.info("Dummy SIPPhone started")

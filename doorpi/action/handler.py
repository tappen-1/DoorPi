#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger(__name__)

class EventHandler:
    def __init__(self):
        logger.debug("EventHandler initialized")
        self.events = {}

    def register_event(self, event_name, source):
        logger.debug(f"Registering event {event_name} from {source}")
        if event_name not in self.events:
            self.events[event_name] = []
        self.events[event_name].append(source)

    def unregister_event(self, event_name):
        logger.debug(f"Unregistering event {event_name}")
        if event_name in self.events:
            del self.events[event_name]

    def fire_event(self, event_name, *args, **kwargs):
        if event_name not in self.events:
            logger.warning(f"No listeners for event {event_name}")
            return
        logger.debug(f"Firing event {event_name}")
        for source in self.events[event_name]:
            try:
                source(*args, **kwargs)
            except Exception as e:
                logger.error(f"Error during event {event_name} execution: {e}")

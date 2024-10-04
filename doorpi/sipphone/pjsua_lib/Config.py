#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser
import logging
import os

logger = logging.getLogger(__name__)

class Config:
    def __init__(self, filename='config.ini'):
        self.filename = filename
        self.config = configparser.ConfigParser()

    def load(self):
        if not os.path.exists(self.filename):
            logger.error(f"Config file {self.filename} does not exist")
            return False

        self.config.read(self.filename)
        logger.info(f"Loaded config file: {self.filename}")
        return True

    def get(self, section, key, fallback=None):
        try:
            return self.config.get(section, key, fallback=fallback)
        except configparser.NoSectionError:
            logger.error(f"Section {section} not found in {self.filename}")
            return fallback
        except configparser.NoOptionError:
            logger.error(f"Option {key} not found in section {section}")
            return fallback

    def set(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, value)
        logger.info(f"Set {key} to {value} in section {section}")

    def save(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)
        logger.info(f"Saved config to {self.filename}")

    def get_keys(self, section):
        if not self.config.has_section(section):
            logger.error(f"Section {section} not found")
            return []
        return self.config.options(section)

    def get_sections(self):
        return self.config.sections()

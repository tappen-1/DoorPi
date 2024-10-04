#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import configparser

REQUIREMENT = {
    'libraries': {
        'configparser': {
            'needed_by': 'config',
            'needed_version': configparser.__version__
        }
    },
    'fulfilled_with_one': True,
    'is_fulfilled': True
}

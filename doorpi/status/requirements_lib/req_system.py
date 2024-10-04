#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import platform

REQUIREMENT = {
    'libraries': {
        'os': {
            'needed_by': 'system',
            'needed_version': platform.system()
        }
    },
    'fulfilled_with_one': True,
    'is_fulfilled': True
}

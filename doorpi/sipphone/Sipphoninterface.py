#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from doorpi.sipphone.from_dummy import Sipphone as Dummy
from doorpi.sipphone.from_pjsua import Sipphone as Pjsua
from doorpi.sipphone.from_linphone import Sipphone as Linphone

AVAILABLE_SIPPHONES = {
    'pjsua': Pjsua,
    'linphone': Linphone,
    'dummy': Dummy
}

def load_sipphone(sipphone_type='dummy'):
    sipphone_type = sipphone_type.lower()
    if sipphone_type not in AVAILABLE_SIPPHONES:
        raise ValueError(f"Sipphone {sipphone_type} not available")
    return AVAILABLE_SIPPHONES[sipphone_type]()

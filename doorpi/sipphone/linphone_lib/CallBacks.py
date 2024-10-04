#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
from time import sleep
import linphone
from doorpi import DoorPi

logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

class LinphoneCallbacks:

    @property
    def used_callbacks(self):
        return {
            'call_state_changed': self.call_state_changed,
            'dtmf_received': self.dtmf_received,
        }

    @property
    def whitelist(self): return DoorPi().config.get_keys('AdminNumbers')

    def is_admin_number(self, remote_uri):
        logger.debug("is_admin_number (%s)", remote_uri)
        for admin_number in self.whitelist:
            if admin_number == "*":
                logger.info("admin numbers are deactivated by using '*' as single number")
                return True
            if "sip:" + admin_number + "@" in remote_uri or "sip:" + admin_number == remote_uri:
                logger.debug("%s is adminnumber %s", remote_uri, admin_number)
                return True
        logger.debug("%s is not an adminnumber", remote_uri)
        return False

    def __init__(self):
        logger.debug("__init__")
        self._last_number_of_calls = 0

        DoorPi().event_handler.register_action('OnSipPhoneDestroy', self.destroy)

        DoorPi().event_handler.register_event('OnCallMediaStateChange', __name__)
        DoorPi().event_handler.register_event('OnCallStateChange', __name__)
        DoorPi().event_handler.register_event('OnCallStateConnect', __name__)
        DoorPi().event_handler.register_event('OnCallStateDisconnect', __name__)
        DoorPi().event_handler.register_event('OnCallStart', __name__)
        DoorPi().event_handler.register_event('OnDTMF', __name__)

        self.__possible_DTMF = DoorPi().config.get_keys('DTMF')
        for DTMF in self.__possible_DTMF:
            DoorPi().event_handler.register_event('OnDTMF_' + DTMF, __name__)

        DoorPi().event_handler('OnCallStart', __name__)

    def destroy(self):
        logger.debug("destroy")
        DoorPi().event_handler.unregister_source(__name__, True)

    def call_state_changed(self, core, call, call_state, message):
        logger.debug("call_state_changed (%s - %s)", call_state, message)
        remote_uri = call.remote_address.as_string_uri_only()
        DoorPi().event_handler('OnCallStateChange', __name__, {
            'remote_uri': remote_uri,
            'call_state': call_state,
            'state': message
        })

        if call_state == linphone.CallState.IncomingReceived:
            self.handle_incoming_call(core, call, remote_uri)
        elif call_state == linphone.CallState.Connected:
            DoorPi().event_handler('OnCallStateConnect', __name__)
        elif call_state == linphone.CallState.StreamsRunning:
            DoorPi().event_handler('OnCallStateConnect', __name__)
        elif call_state == linphone.CallState.End:
            DoorPi().event_handler('OnCallStateDisconnect', __name__)

    def handle_incoming_call(self, core, call, remote_uri):
        if self.is_admin_number(remote_uri):
            DoorPi().event_handler('OnCallIncoming', __name__, {'remote_uri': remote_uri})
            core.accept_call(call)
        else:
            DoorPi().event_handler('OnCallReject', __name__)
            core.decline_call(call, linphone.Reason.Declined)

    def dtmf_received(self, core, call, digits):
        digits = chr(digits)
        DoorPi().event_handler('OnDTMF', __name__, {'digits': digits})
        self.__DTMF += digits
        for DTMF in self.__possible_DTMF:
            if self.__DTMF.endswith(DTMF[1:-1]):
                DoorPi().event_handler('OnDTMF_' + DTMF, __name__, {
                    'remote_uri': call.remote_address.as_string_uri_only(),
                    'DTMF': self.__DTMF
                })

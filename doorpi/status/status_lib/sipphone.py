#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

def get(*args, **kwargs):
    try:
        if not kwargs.get('name'):
            kwargs['name'] = ['']
        if not kwargs.get('value'):
            kwargs['value'] = ['']

        sipphone = kwargs['DoorPiObject'].sipphone

        status = {}
        for name_requested in kwargs['name']:
            sipphone.thread_register('status_thread')

            if name_requested == 'name':
                status['name'] = sipphone.name

            if name_requested == 'sound_codecs':
                status['sound_codecs'] = sipphone.sound_codecs
            if name_requested == 'sound_devices':
                status['sound_devices'] = sipphone.sound_devices

            if name_requested == 'sound_enable':
                status['sound_enable'] = bool(sipphone.sound_codecs and sipphone.sound_devices)

            if name_requested == 'video_codecs':
                status['video_codecs'] = sipphone.video_codecs
            if name_requested == 'video_devices':
                status['video_devices'] = sipphone.video_devices

            if name_requested == 'video_enable':
                status['video_enable'] = bool(sipphone.video_codecs and sipphone.video_devices)

            if name_requested == 'recorder':
                status['has_recorder'] = bool(sipphone.recorder)
                if status['has_recorder']:
                    status['recorder_filename'] = sipphone.recorder.record_filename
                    status['recorder_parsed_filename'] = sipphone.recorder.parsed_record_filename

            if name_requested == 'player':
                status['has_player'] = bool(sipphone.player)
                if status['has_player']:
                    status['player_filename'] = sipphone.player.player_filename

            if name_requested == 'current_call':
                status['current_call'] = sipphone.current_call_dump

        return status
    except Exception as exp:
        logger.exception(exp)
        return {'Error': 'could not create '+str(__name__)+' object - '+str(exp)}

def is_active(doorpi_object):
    return bool(doorpi_object.sipphone)

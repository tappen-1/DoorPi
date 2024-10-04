#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

import os
from doorpi import DoorPi
from doorpi.sipphone.AbstractBaseClass import PlayerAbstractBaseClass

class PjsuaPlayer(PlayerAbstractBaseClass):

    __player_id = None
    __slot_id = None

    __player_filename = ''
    __last_player_filename = ''

    @property
    def player_filename(self): return self.__player_filename

    @property
    def parsed_player_filename(self): return DoorPi().parse_string(self.__player_filename)

    @property
    def last_player_filename(self): return self.__last_player_filename

    def __init__(self):
        self.__player_filename = DoorPi().config.get('DoorPi', 'player', '!BASEPATH!/player/default.wav')
        if self.__player_filename == '':
            logger.debug('no player found in config at section DoorPi and key player')
            return

        DoorPi().event_handler.register_event('OnPlayerStarted', __name__)
        DoorPi().event_handler.register_event('OnPlayerStopped', __name__)
        DoorPi().event_handler.register_event('OnPlayerCreated', __name__)

        if DoorPi().config.get_bool('DoorPi', 'play_while_dialing', 'False'):
            DoorPi().event_handler.register_action('OnSipPhoneMakeCall', self.start)
        else:
            DoorPi().event_handler.register_action('OnCallStateConnect', self.start)

        DoorPi().event_handler.register_action('OnCallStateDisconnect', self.stop)

        DoorPi().event_handler('OnPlayerCreated', __name__)

    def start(self):
        if self.__player_filename == '':
            return

        if self.__player_id is not None:
            logger.trace('player already created as player_id %s and playing %s', self.__player_id, self.last_player_filename)
            return

        DoorPi().sipphone.lib.thread_register('PjsuaPlayer_start_thread')

        if self.__player_filename != '':
            self.__last_player_filename = DoorPi().parse_string(self.__player_filename)
            if not os.path.exists(os.path.dirname(self.__last_player_filename)):
                logger.info('Path %s does not exist - creating it now', os.path.dirname(self.__last_player_filename))
                os.makedirs(os.path.dirname(self.__last_player_filename))

            logger.debug('starting playing %s', self.__last_player_filename)
            self.__player_id = DoorPi().sipphone.lib.create_player(self.__last_player_filename, loop=False)
            self.__slot_id = DoorPi().sipphone.lib.player_get_slot(self.__player_id)
            DoorPi().sipphone.lib.conf_connect(self.__slot_id, 0)
            DoorPi().event_handler('OnPlayerStarted', __name__)

    def stop(self):
        if self.__player_id is not None:
            DoorPi().sipphone.lib.thread_register('PjsuaPlayer_stop_thread')
            logger.debug('stopping playing %s', self.__last_player_filename)
            DoorPi().sipphone.lib.conf_disconnect(self.__slot_id, 0)
            DoorPi().sipphone.lib.player_destroy(self.__player_id)
            self.__player_id = None
            self.__slot_id = None
            DoorPi().event_handler('OnPlayerStopped', __name__)

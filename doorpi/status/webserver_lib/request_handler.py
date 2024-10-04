#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import logging
logger = logging.getLogger(__name__)
logger.debug("%s loaded", __name__)

import os
from mimetypes import guess_type
from http.server import BaseHTTPRequestHandler  # In Python 3 geändert
import cgi
from urllib.parse import urlparse, parse_qs  # In Python 3 geändert
import re
import json
from urllib.request import urlopen as load_online_fallback  # In Python 3 geändert
from urllib.parse import unquote_plus  # In Python 3 geändert

from doorpi.action.base import SingleAction
import doorpi
from request_handler_static_functions import *

VIRTUELL_RESOURCES = [
    '/mirror',
    '/status',
    '/control/trigger_event',
    '/control/config_value_get',
    '/control/config_value_set',
    '/control/config_value_delete',
    '/control/config_save',
    '/control/config_get_configfile',
    '/help/modules.overview.html'
]

DOORPIWEB_SECTION = 'DoorPiWeb'

class WebServerLoginRequired(Exception): pass
class WebServerRequestHandlerShutdownAction(SingleAction): pass

class DoorPiWebRequestHandler(BaseHTTPRequestHandler):

    @property
    def conf(self): return self.server.config

    def log_error(self, format, *args): logger.error("[%s] %s", self.client_address[0], args)
    def log_message(self, format, *args): logger.debug("[%s] %s", self.client_address[0], args)

    @staticmethod
    def prepare():
        doorpi.DoorPi().event_handler.register_event('OnWebServerRequest', __name__)
        doorpi.DoorPi().event_handler.register_event('OnWebServerRequestGet', __name__)
        doorpi.DoorPi().event_handler.register_event('OnWebServerRequestPost', __name__)
        doorpi.DoorPi().event_handler.register_event('OnWebServerVirtualResource', __name__)
        doorpi.DoorPi().event_handler.register_event('OnWebServerRealResource', __name__)

        # for do_control
        doorpi.DoorPi().event_handler.register_event('OnFireEvent', __name__)
        doorpi.DoorPi().event_handler.register_event('OnConfigKeySet', __name__)
        doorpi.DoorPi().event_handler.register_event('OnConfigKeyDelete', __name__)

    @staticmethod
    def destroy():
        doorpi.DoorPi().event_handler.unregister_source( __name__, True)

    def do_GET(self):
        if not self.server.keep_running: return

        parsed_path = urlparse(self.path)

        if parsed_path.path == "/":
            return self.return_redirection('dashboard/pages/index.html')

        if self.authentication_required(): return self.login_form()

        if parsed_path.path in VIRTUELL_RESOURCES:
            return self.create_virtual_resource(parsed_path, parse_qs(urlparse(self.path).query))
        else: return self.real_resource(parsed_path.path)

    def do_control(self, control_order, para):
        result_object = dict(
            success = False,
            message = 'unknown error'
        )
        logger.debug(json.dumps(para, sort_keys = True, indent = 4))

        try:
            for parameter_name in para.keys():
                try: para[parameter_name] = unquote_plus(para[parameter_name][0])
                except KeyError: para[parameter_name] = ''
                except IndexError: para[parameter_name] = ''

            if control_order == "trigger_event":
                result_object['message'] = doorpi.DoorPi().event_handler.fire_event_synchron(**para)
                if result_object['message'] is True:
                    result_object['success'] = True
                    result_object['message'] = "fire Event was success"
                else:
                    result_object['success'] = False
            elif control_order == "config_value_get":
                result_object['success'] = True
                result_object['message'] = control_config_get_value(**para)
            elif control_order == "config_value_set":
                result_object['success'] = control_config_set_value(**para)
                result_object['message'] = "config_value_set %s" % (
                    'success' if result_object['success'] else 'failed'
                )
            elif control_order == "config_value_delete":
                result_object['success'] = control_config_delete_key(**para)
                result_object['message'] = "config_value_delete %s" % (
                    'success' if result_object['success'] else 'failed'
                )
            elif control_order == "config_save":
                result_object['success'] = control_config_save(**para)
                result_object['message'] = "config_save %s" % (
                    'success' if result_object['success'] else 'failed'
                )
            elif control_order == "config_get_configfile":
                result_object['message'] = control_config_get_configfile()
                result_object['success'] = True if result_object['message'] != "" else False

        except Exception as exp:
            result_object['message'] = str(exp)

        return result_object

    def clear_parameters(self, raw_parameters):
        if 'module' not in raw_parameters.keys(): raw_parameters['module'] = []
        if 'name' not in raw_parameters.keys(): raw_parameters['name'] = []
        if 'value' not in raw_parameters.keys(): raw_parameters['value'] = []
        return raw_parameters

    def create_virtual_resource(self, path, raw_parameters):
        return_object = {}
        try:
            if path.path == '/mirror':
                return_object = self.create_mirror()
                raw_parameters['output'] = "string"
            elif path.path == '/status':
                raw_parameters = self.clear_parameters(raw_parameters)
                return_object = doorpi.DoorPi().get_status(
                    modules = raw_parameters['module'],
                    name = raw_parameters['name'],
                    value = raw_parameters['value']
                ).dictionary
            elif path.path.startswith('/control/'):
                return_object = self.do_control(path.path.split('/')[-1], raw_parameters)
            elif path.path == '/help/modules.overview.html':
                raw_parameters = self.clear_parameters(raw_parameters)
                return_object, mime = self.get_file_content('/dashboard/parts/modules.overview.html')
                return_object = self.parse_content(
                    return_object,
                    MODULE_AREA_NAME = raw_parameters['module'][0] or '',
                    MODULE_NAME = raw_parameters['name'][0] or ''
                )
                raw_parameters['output'] = "html"
        except Exception as exp: return_object = dict(error_message = str(exp))

        if 'output' not in raw_parameters.keys(): raw_parameters['output'] = ''
        return self.return_virtual_resource(return_object, raw_parameters['output'])

    def return_virtual_resource(self, prepared_object, return_type = 'json'):
        if isinstance(return_type, list) and len(return_type) > 0: return_type = return_type[0]

        if return_type in ["json", "default"]:
            return  self.return_message(json.dumps(prepared_object), "application/json; charset=utf-8")
        if return_type in ["json_parsed", "json.parsed"]:
            return  self.return_message(self.parse_content(json.dumps(prepared_object)), "application/json; charset=utf-8")
        elif return_type in ["json_beautified", "json.beautified", "beautified.json"]:
            return  self.return_message(json.dumps(prepared_object, sort_keys=True, indent=4), "application/json; charset=utf-8")
        elif return_type in ["json_beautified_parsed", "json.beautified.parsed", "beautified.json.parsed", ""]:
            return  self.return_message(self.parse_content(json.dumps(prepared_object, sort_keys=True, indent=4)), "application/json; charset=utf-8")
        elif return_type in ["string", "plain", "str"]:
            return self.return_message(str(prepared_object))
        elif return_type in ["repr"]:
            return self.return_message(repr(prepared_object))
        elif return_type == 'html':  # Geändert von is zu ==
            return self.return_message(prepared_object, 'text/html; charset=utf-8')
        else:
            try: return self.return_message(repr(prepared_object))
            except: return self.return_message(str(prepared_object))

    # Der restliche Code bleibt unverändert

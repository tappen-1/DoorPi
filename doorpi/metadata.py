# -*- coding: utf-8 -*-
"""Project metadata

Information describing the project.
"""
import os

# Das Paketname, das auch der "UNIX-Name" für das Projekt ist.
package = 'DoorPi'
project = "VoIP Door-Intercomstation with Raspberry Pi"
project_no_spaces = project.replace(' ', '')
version = '2.5.1'
description = 'provide intercomstation to the doorstation by VoIP'
keywords = ['intercom', 'VoIP', 'doorstation', 'home automation', 'IoT']
authors = ['Thomas Meissner']
authors_emails = ['motom001@gmail.com']
authors_string = ', '.join(authors)
author_strings = [f'{name} <{email}>' for name, email in zip(authors, authors_emails)]

supporters = [
    'Phillip Munz <office@businessaccess.info>',
    'Hermann Dötsch <doorpi1@gmail.com>',
    'Dennis Häußler <haeusslerd@outlook.com>',
    'Hubert Nusser <hubsif@gmx.de>',
    'Michael Hauer <frrr@gmx.at>',
    'Andreas Schwarz <doorpi@schwarz-ketsch.de>',
    'Max Rößler <max_kr@gmx.de>',
    'missing someone? -> sorry -> mail me'
]
supporter_string = '\n'.join(supporters)
copyright = f"{authors[0]}, 2014-2015"
license = 'CC BY-NC 4.0'
url = 'https://github.com/motom001/DoorPi'
url_raw = 'https://raw.githubusercontent.com/motom001/DoorPi'

# erstellt mit: http://patorjk.com/software/taag/#p=display&f=Ogre&t=DoorPi
epilog = '''
    ___                  ___ _
   /   \___   ___  _ __ / _ (_)  {project}
  / /\ / _ \ / _ \| '__/ /_)/ |  version:   {version}
 / /_// (_) | (_) | | / ___/| |  license:   {license}
/___,' \___/ \___/|_| \/    |_|  URL:       <{url}>

Authors:    {authors}
Supporter:  {supporters}
'''.format(
    project=project,
    version=version,
    license=license,
    url=url,
    authors='\n'.join(author_strings),
    supporters='\n            '.join(supporters)
)

if os.name == 'posix':
    doorpi_path = os.path.join('/usr/local/etc', package)

    pidfile = f'/var/run/{package.lower()}.pid'

    daemon_name = package.lower()
    daemon_folder = '/etc/init.d'
    daemon_file = os.path.join(daemon_folder, daemon_name)

    daemon_online_template = f'{url_raw}/master/doorpi/docs/service/doorpi.tpl'

    daemon_args = '--configfile $DOORPI_PATH/conf/doorpi.ini'
    doorpi_executable = '/usr/local/bin/doorpi_cli'
    log_folder = f'{doorpi_path}/log'
    
    if not os.path.exists(doorpi_path):
        os.makedirs(doorpi_path)
else:
    raise Exception('OS unknown')

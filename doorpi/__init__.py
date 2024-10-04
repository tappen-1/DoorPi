# -*- coding: utf-8 -*-
"""provide intercomstation to the doorstation by VoIP"""

from doorpi import metadata

__version__ = metadata.version
__author__ = metadata.authors[0]
__license__ = metadata.license
__copyright__ = metadata.copyright

# Lazy loading von DoorPi, um zirkuläre Abhängigkeit zu vermeiden
def get_doorpi_instance():
    from doorpi.doorpi import DoorPi
    return DoorPi()

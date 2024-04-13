#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import sys
from logging.config import fileConfig
from smart_planning.controller.DatabaseController import *
from smart_planning.sel import *

fileConfig('smart_planning/config/logging_config.ini')


def main():
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'smart_planning.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    database_controller = DatabaseController()
    database_controller.create_schema()
    sel_heuristic('volga', ["room-01", "room-02", "room-03"],
                  ["temperature-control-application"], ["info-flow-01"],
                  ["ifr-flow-01", "ifr-flow-02", "ifr-flow-03"], 20, 10)
    #main()

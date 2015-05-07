#!/usr/bin/env python
import os
import sys

pwd = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0,  os.path.dirname(pwd) )

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)

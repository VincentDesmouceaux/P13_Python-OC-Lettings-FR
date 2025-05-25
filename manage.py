#!/usr/bin/env python
"""Django management entry‑point."""
import os
import sys


def main() -> None:
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "oc_lettings_site.settings")
    from django.core.management import execute_from_command_line  # type: ignore
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

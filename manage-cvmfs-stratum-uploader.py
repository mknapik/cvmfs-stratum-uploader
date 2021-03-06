#!/usr/bin/env python
import logging
import os
import sys

logger = logging.getLogger(__name__)


def main():
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'uploader.settings')

    if len(sys.argv) > 1 and sys.argv[1] == 'test':
        os.environ.setdefault('DJANGO_CONFIGURATION', 'test')
        os.environ.setdefault('REUSE_DB', '1')
    else:
        os.environ.setdefault('DJANGO_CONFIGURATION', 'dev')

    logger.debug('DJANGO_SETTINGS_MODULE = %s' % os.environ['DJANGO_SETTINGS_MODULE'])
    logger.debug('DJANGO_CONFIGURATION = %s' % os.environ['DJANGO_CONFIGURATION'])

    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()

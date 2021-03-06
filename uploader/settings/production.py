"""
This config uses ConfigParser to load settings from config file.

The config file is divided into 6 sections: path, url, security, debug, apps and misc.
Each section has a validation against specific set of options.
To see what options are available look for OPTIONS_AVAILABLE dictionary.

All options which were not listed in OPTIONS_AVAILABLE can be passed in 'misc' section.
Keep in mind that only simple key-value options can be passed without modifying load_cfg() function.
"""
# noinspection PyUnresolvedReferences
import logging
import re
from uploader.settings import common
from uploader.settings.common import *

logger = logging.getLogger(__name__)

DEBUG = True
TEMPLATE_DEBUG = DEBUG

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        # Add 'postgresql_psycopg2', 'postgresql', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': '%s/db/cvmfs-stratum-uploader.sqlite3' % PROJECT_ROOT, # Or path to database file if using sqlite3.
        'USER': '', # Not used with sqlite3.
        'PASSWORD': '', # Not used with sqlite3.
        'HOST': '', # Set to empty string for localhost. Not used with sqlite3.
        'PORT': '', # Set to empty string for default. Not used with sqlite3.
    }
}

OPTIONS_AVAILABLE = {
    'path': ['PROJECT_ROOT', 'MEDIA_ROOT', 'STATIC_ROOT'],
    'url': ['HOSTNAME', 'MEDIA_URL', 'STATIC_URL'],
    'security': ['SECRET_KEY', 'CSRF_MIDDLEWARE_SECRET', 'ALLOWED_HOSTS'],
    'debug': ['DEBUG', 'TEMPLATE_DEBUG', 'VIEW_TEST', 'INTERNAL_IPS', 'SKIP_CSRF_MIDDLEWARE'],
    'apps': ['ADD[0-9]+'],
    'misc': None,
}


def load_cfg():
    import ConfigParser
    import os

    def cast(value):
        if value.isdigit():
            return int(value)
        elif value.lower() in ('true', 'false'):
            return value.lower() == 'true'
        else:
            return value

    def set_option(option, value):
        logger.debug('set %s = %s' % (option.upper(), value))
        globals()[option.upper()] = value

    LIST_TYPES = (
        ('debug', 'INTERNAL_IPS',),
        ('security', 'ALLOWED_HOSTS',),
    )

    config = ConfigParser.SafeConfigParser()
    configs = ['/var/www/cvmfs-stratum-uploader/application.cfg',
               os.path.expanduser('~/.cvmfs-stratum-uploader.cfg'), ]
    if os.environ.has_key('DJANGO_CONFIG_FILE'):
        configs.append(os.environ.get('DJANGO_CONFIG_FILE'))
    # configs are read one by one
    config.read(configs)

    for section in config.sections():
        if section == 'database':
            default_db = {}
            for option in config.options(section):
                default_db[option.upper()] = config.get(section, option)
            set_option('DATABASES', {'default': default_db})
        elif section == 'logging':
            logger.error('TBD')
            raise NotImplementedError('Logging section has not been handled yet!')
        elif section == 'apps':
            for option in config.options(section):
                option = option.upper()
                value = config.get(section, option)

                set_option('INSTALLED_APPS', common.INSTALLED_APPS + (value,))
        else:
            if section not in OPTIONS_AVAILABLE.keys():
                raise ValueError('Unrecognized section: [%s]. Perhaps, [misc] should be used instead.' % section)

            for option in config.options(section):
                option = option.upper()
                if OPTIONS_AVAILABLE[section] is not None and option not in OPTIONS_AVAILABLE[section]:
                    raise ValueError('Option "%s" is not available for section [%s]' % (option, section))
                value = config.get(section, option)

                if (section, option,) in LIST_TYPES:
                    set_option(option, tuple(re.split(',\s*', value)))
                else:
                    set_option(option, cast(value))

load_cfg()

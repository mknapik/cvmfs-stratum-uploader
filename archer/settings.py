# Django settings for archer project.

DEBUG = True
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('vwa13376', 'michael.knapik@stfc.ac.uk'),
)
TEMPLATE_CONTEXT_PROCESSORS = ("django.contrib.auth.context_processors.auth",
                               "django.core.context_processors.debug",
                               "django.core.context_processors.i18n",
                               "django.core.context_processors.media",
                               "django.core.context_processors.static",
                               "django.core.context_processors.tz",
                               "django.contrib.messages.context_processors.messages",
                               'multiuploader.context_processors.booleans')

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'dev.sqlite3', # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': '',
        'PASSWORD': '',
        'HOST': '', # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '', # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'UTC'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = ''

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://example.com/media/", "http://media.example.com/"
MEDIA_URL = ''

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# URL prefix for static files.
# Example: "http://example.com/static/", "http://static.example.com/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = (
# Put strings here, like "/home/html/static" or "C:/www/django/static".
# Always use forward slashes, even on Windows.
# Don't forget to use absolute paths, not relative paths.
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'apksigo!uh4gth@7nco7y2biavj=0fxd0b3@2!ax6*rb29fq=w'

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    #     'django.template.loaders.eggs.Loader',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'archer.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'archer.wsgi.application'

import os

TEMPLATE_DIRS = (os.path.join(os.path.dirname(__file__), '..', 'templates').replace('\\', '/'),)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Uncomment the next line to enable the admin:
    # Themes:
    # 'grappelli',
    # 'bootstrap_admin',
    # 'django_admin_bootstrapped',
    'django.contrib.admin',
    # Uncomment the next line to enable admin documentation:
    # 'django.contrib.admindocs',
    'uploader',
    'gunicorn',
    'bootstrap_toolkit',
    'django_extensions',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

## Multiuploader configuration
MULTIUPLOADER_FILES_FOLDER = 'uploads'
MULTIUPLOADER_FILE_EXPIRATION_TIME = '3600'
MULTIUPLOADER_FORMS_SETTINGS = {
    'default': {
        'FILE_TYPES': ["txt", "zip", "jpg", "jpeg", "flv", "png"],
        'CONTENT_TYPES': [
            'image/jpeg',
            'image/png',
            'application/msword',
            'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
            'application/vnd.ms-excel',
            'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            'application/vnd.ms-powerpoint',
            'application/vnd.openxmlformats-officedocument.presentationml.presentation',
            'application/vnd.oasis.opendocument.text',
            'application/vnd.oasis.opendocument.spreadsheet',
            'application/vnd.oasis.opendocument.presentation',
            'text/plain',
            'text/rtf',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True,
    },
    'images': {
        'FILE_TYPES': ['jpg', 'jpeg', 'png', 'gif', 'svg', 'bmp', 'tiff', 'ico'],
        'CONTENT_TYPES': [
            'image/gif',
            'image/jpeg',
            'image/pjpeg',
            'image/png',
            'image/svg+xml',
            'image/tiff',
            'image/vnd.microsoft.icon',
            'image/vnd.wap.wbmp',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True,
    },
    'video': {
        'FILE_TYPES': ['flv', 'mpg', 'mpeg', 'mp4', 'avi', 'mkv', 'ogg', 'wmv', 'mov', 'webm'],
        'CONTENT_TYPES': [
            'video/mpeg',
            'video/mp4',
            'video/ogg',
            'video/quicktime',
            'video/webm',
            'video/x-ms-wmv',
            'video/x-flv',
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True,
    },
    'audio': {
        'FILE_TYPES': ['mp3', 'mp4', 'ogg', 'wma', 'wax', 'wav', 'webm'],
        'CONTENT_TYPES': [
            'audio/basic',
            'audio/L24',
            'audio/mp4',
            'audio/mpeg',
            'audio/ogg',
            'audio/vorbis',
            'audio/x-ms-wma',
            'audio/x-ms-wax',
            'audio/vnd.rn-realaudio',
            'audio/vnd.wave',
            'audio/webm'
        ],
        'MAX_FILE_SIZE': 10485760,
        'MAX_FILE_NUMBER': 5,
        'AUTO_UPLOAD': True,
    }}
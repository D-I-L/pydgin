"""
Django settings for pydgin project.

Generated by 'django-admin startproject' using Django 1.8.1.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.8/ref/settings/
"""
from pydgin.settings_secret import *
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(__file__)

sys.path.insert(0, os.path.join(PROJECT_DIR, 'local_apps'))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
TESTMODE = sys.argv[1:2] == ['test']

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'criteria',
    'data_pipeline',
    'elastic',
    'search_engine',
    'gene',
    'marker',
    'disease',
    'region',
    'rest_framework',
    'rest_framework_swagger',
    'rest_framework.authtoken',
    'pydgin_auth',
    'auth_test',
    'mod_wsgi.server',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'pydgin_auth.login_required_middleware.LoginRequiredMiddleware',
)

ROOT_URLCONF = 'pydgin.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'pydgin/templates/')
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    )
}

WSGI_APPLICATION = 'pydgin.wsgi.application'

AUTH_PROFILE_MODULE = "pydgin_auth.UserProfile"
# Import Applicaton-specific Settings
PYDGIN_AUTH_APPS_BASE_NAME = 'pydgin_auth'
for app in INSTALLED_APPS:
    if app.startswith(PYDGIN_AUTH_APPS_BASE_NAME):
        try:
            app_module = __import__(app, globals(), locals(), ["settings"])
            app_settings = getattr(app_module, "settings", None)
            for setting in dir(app_settings):
                if setting == setting.upper():
                    locals()[setting] = getattr(app_settings, setting)
        except ImportError:
            pass


########
# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

# DATABASES = {
#    'default': {
#        'ENGINE': 'django.db.backends.sqlite3',
#        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
#    }
# }


# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

# TIME_ZONE = 'UTC'
TIME_ZONE = 'Europe/London'
USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "pydgin/static"),
)
STATIC_ROOT = os.path.join(PROJECT_DIR, 'apache')

if not DEBUG:
    STATICFILES_STORAGE = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'

# writes all request logging from the django.request logger to a local file
LOG_FILE = os.path.join(BASE_DIR, 'log/pydgin.log')
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': "[%(asctime)s] %(levelname)s [%(name)s:%(lineno)s] %(message)s",
            'datefmt': "%d/%b/%Y %H:%M:%S"
        },
        'simple': {
            'format': '%(levelname)s %(message)s'
        },
    },
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'when': 'midnight',
            'interval': 1,
            'backupCount': 10,
            'filename': LOG_FILE,
            'formatter': 'verbose',
        },
        'null': {
            'level': 'DEBUG',
            'class': 'logging.NullHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'elastic': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'data_pipeline': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'search_engine': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'marker': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
        'pydgin_auth': {
            'handlers': ['file', 'console'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}


URL_LINKS = {
    "hgnc":
        {
            "link": "http://www.genenames.org/cgi-bin/gene_symbol_report?hgnc_id=HGNC:",
            "about": "HUGO Gene Nomenclature Committee at the European Bioinformatics Institute"
        },
    "vega":
        {
            "link": "http://vega.sanger.ac.uk/Homo_sapiens/Gene/Summary?db=core;g=",
            "about": "Repository for high-quality gene models produced by the manual annotation of vertebrate genomes"
        },
    "trembl":
        {
            "link": "http://www.uniprot.org/uniprot/",
            "about": "UniProt: resource of protein sequence and functional information",
        },
    "swissprot":
        {
            "link": "http://www.uniprot.org/uniprot/",
            "about": "UniProt: resource of protein sequence and functional information",
        },
    "mim":
        {
            "link": "http://omim.org/entry/",
            "about": "Online Mendelian Inheritance in Man"
        },
    "entrez":
        {
            "link": "http://www.ncbi.nlm.nih.gov/gene?cmd=retrieve&dopt=full_repor&list_uids=",
            "about": "NCBI database"
        },
    "hprd":
        {
            "link": "http://www.hprd.org/protein/",
            "about": "Human Protein Reference Database"
        },
    "ensembl":
        {
            "link": "http://dec2015.archive.ensembl.org/Homo_sapiens/geneview?gene=",
            "about": "Ensembl project"
        }
}

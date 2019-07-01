from os import environ

from ..exceptions import MissingEnvironmentVariable


# Configuration
DATABASE_URL = environ.get('DATABASE_URL')
CFPLAND_URL = 'https://api.cfpland.com/v0/conferences'
ENVIRONMENT = environ.get('ENVIRONMENT')
TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
TELEGRAM_CFPLAND_CHANNEL = environ.get('TELEGRAM_CFPLAND_CHANNEL')

if not ENVIRONMENT:
    raise MissingEnvironmentVariable('ENVIRONMENT')

if not TELEGRAM_TOKEN:
    raise MissingEnvironmentVariable('TELEGRAM_TOKEN')

if not TELEGRAM_CFPLAND_CHANNEL:
    raise MissingEnvironmentVariable('TELEGRAM_CFPLAND_CHANNEL')


# Logging
COULD_NOT_CREATE_CFP = 'could not create CFP'
COULD_NOT_FORMAT_DATES_CFP = 'could not formate dates for CFP'
CREATED_CFP = 'created CFP'
SENT_TO_TELEGRAM_CHANNEL = 'sent new CFP to telegram channel'

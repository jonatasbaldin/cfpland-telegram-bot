from os import environ

from ..exceptions import MissingEnvironmentVariable

from ssm_cache import SSMParameterGroup


# Configuration
CFPLAND_URL = 'https://api.cfpland.com/v0/conferences'
ENVIRONMENT = environ.get('ENVIRONMENT').lower()  # prod, dev, test
TELEGRAM_CFPLAND_CHANNEL = environ.get('TELEGRAM_CFPLAND_CHANNEL')


# SSM Parameters
if ENVIRONMENT in ['prod', 'dev']:
    group = SSMParameterGroup(base_path=f'/CFPLAND/{ENVIRONMENT.upper()}')
    DATABASE_URL = group.parameter('/DATABASE_URL').value
    TELEGRAM_TOKEN = group.parameter('/TELEGRAM_TOKEN').value

# Load from env var when testing
if ENVIRONMENT == 'test':
    DATABASE_URL = environ.get('DATABASE_URL')
    TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')


if not ENVIRONMENT:
    raise MissingEnvironmentVariable('ENVIRONMENT')

if not TELEGRAM_TOKEN:
    raise MissingEnvironmentVariable('TELEGRAM_TOKEN')

if not TELEGRAM_CFPLAND_CHANNEL:
    raise MissingEnvironmentVariable('TELEGRAM_CFPLAND_CHANNEL')


# Logging
COULD_NOT_CREATE_CFP = 'could not create CFP'
COULD_NOT_FORMAT_DATES_CFP = 'could not formate dates for CFP'
COULD_NOT_UPDATE_BOT_INFORMATION = 'could not update bot information'
CREATED_CFP = 'created CFP'
SENT_TO_TELEGRAM_CHANNEL = 'sent new CFP to telegram channel'

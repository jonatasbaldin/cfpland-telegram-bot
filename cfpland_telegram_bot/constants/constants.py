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
    IOPIPE_TOKEN = group.parameter('/IOPIPE_TOKEN').value
    TELEGRAM_TOKEN = group.parameter('/TELEGRAM_TOKEN').value
    DYNAMODB_TABLE = group.parameter('/DYNAMODB_TABLE').value

# Load from env var when testing
if ENVIRONMENT == 'test':
    DATABASE_URL = environ.get('DATABASE_URL')
    IOPIPE_TOKEN = environ.get('IOPIPE_TOKEN')
    TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
    DYNAMODB_TABLE = environ.get('DYNAMODB_TABLE')


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
CREATED_CFP_DYNAMODB = 'created CFP dynamodb'
SENT_TO_TELEGRAM_CHANNEL = 'sent new CFP to telegram channel'

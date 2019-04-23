from os import environ
from exceptions import MissingEnvironmentVariable

DATABASE_URL = environ.get('DATABASE_URL')
CFPLAND_FEED_URL = 'https://feeds.cfpland.com/v2/rss/cfps'
ENVIRONMENT = environ.get('ENVIRONMENT', 'DEV')
TELEGRAM_TOKEN = environ.get('TELEGRAM_TOKEN')
TELEGRAM_CFPLAND_CHANNEL = environ.get('TELEGRAM_CFPLAND_CHANNEL')

if not TELEGRAM_TOKEN:
    raise MissingEnvironmentVariable('TELEGRAM_TOKEN')

if not TELEGRAM_CFPLAND_CHANNEL:
    raise MissingEnvironmentVariable('TELEGRAM_CFPLAND_CHANNEL')

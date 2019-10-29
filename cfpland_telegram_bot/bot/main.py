from collections import namedtuple
import re

from .bot import bot
from ..constants import SENT_TO_TELEGRAM_CHANNEL, TELEGRAM_CFPLAND_CHANNEL
from ..logger import logger
from ..models import CFP


Cfp = namedtuple(
    'CFP',
    ['title', 'category', 'cfp_end_date', 'perk_list', 'event_start_date', 'location', 'link'],
)


def telegram_bot(event, context):
    lambda_logger = logger.bind(lambda_event=event, lambda_context=vars(context))
    body = event.get('body')

    if event.get('httpMethod') == 'POST' and body:
        bot.update(body)

        lambda_logger.info({
            'message_received': bot.message_received,
            'chat_id': bot.chat_id,
        })

        if bot.message_received == '/start':
            bot.send_start_message(bot.chat_id)

        latest_category_match = re.search(r'^(/latest) (\w+)$', bot.message_received)
        if latest_category_match:
            category = latest_category_match.groups()[-1].lower()

            cfps = CFP.get_latest_by_category(category)
            if cfps:
                for cfp in cfps:
                    message = bot.format_cfp(cfp)
                    bot.send_message(bot.chat_id, message)
            else:
                message = (
                    f'Sorry, I could not find any {category} CFPs 😔\n\n'
                    f'You can find all the available categories with the /categories command!'
                )
                bot.send_message(bot.chat_id, message)

        if bot.message_received == '/latest':
            for cfp in CFP.get_latest():
                message = bot.format_cfp(cfp)
                bot.send_message(bot.chat_id, message)

        if bot.message_received == '/categories':
            message = '👉  *Here are the categories available:*\n\n'
            for entry in CFP.get_categories():
                message = message + entry.category + '\n'

            bot.send_message(bot.chat_id, message)

        return bot.ok_response()

    return bot.error_response()


def send_telegram_messages_to_channel(event, context):
    """
    Send a CFP message to the Telegram distribution channel.
    The `event` is a DynamoDB stream.
    """

    lambda_logger = logger.bind(lambda_event=event, lambda_context=vars(context))

    for item in event.get('Records'):
        cfp_data = item.get('dynamodb').get('NewImage')
        title = cfp_data.get('title').get('S')
        category = cfp_data.get('category').get('S')
        cfp_end_date = cfp_data.get('cfpEndDate').get('S')
        perk_list = cfp_data.get('perkList').get('S')
        event_start_date = cfp_data.get('eventStartDate').get('S')
        location = cfp_data.get('location').get('S')
        link = cfp_data.get('link').get('S')

        cfp = Cfp(
            title,
            category,
            cfp_end_date,
            perk_list,
            event_start_date,
            location,
            link,
        )

        message = bot.format_cfp(cfp)
        bot.send_message(TELEGRAM_CFPLAND_CHANNEL, message)

        lambda_logger.info(
            {
                'description': SENT_TO_TELEGRAM_CHANNEL,
                'cfp_title': cfp.title,
                'chat_id': TELEGRAM_CFPLAND_CHANNEL,
            }, code=SENT_TO_TELEGRAM_CHANNEL,
        )


def set_telegram_webhook(event, context):
    webhook = bot.set_webhook(event)

    if webhook:
        return bot.ok_response()

    return bot.error_response()

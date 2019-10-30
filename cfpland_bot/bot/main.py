import re

from .bot import bot
from ..constants import (
    COULD_NOT_UPDATE_BOT_INFORMATION,
    SENT_TO_TELEGRAM_CHANNEL,
    TELEGRAM_CFPLAND_CHANNEL,
)
from ..logger import logger
from ..models import CFP


def telegram_bot(event, context):
    lambda_logger = logger.bind(lambda_event=event, lambda_context=vars(context))
    body = event.get('body')

    if event.get('httpMethod') == 'POST' and body:
        try:
            bot.update(body)
        except AttributeError as exception:
            logger.exception(
                {
                    'description': COULD_NOT_UPDATE_BOT_INFORMATION,
                    'exception': exception,
                },
                code=COULD_NOT_UPDATE_BOT_INFORMATION, exc_info=True,
            )

            return bot.error_response()

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
    """

    lambda_logger = logger.bind(lambda_event=event, lambda_context=vars(context))

    not_sent = CFP.get_not_sent_telegram()

    for cfp in not_sent:
        message = bot.format_cfp(cfp)
        bot.send_message(TELEGRAM_CFPLAND_CHANNEL, message)
        cfp.sent_on_telegram()

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

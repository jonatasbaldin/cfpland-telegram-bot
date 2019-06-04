import re

from loguru import logger

from bot import TelegramBot, bot
from constants import TELEGRAM_CFPLAND_CHANNEL
from models import CFP, DB
from parser import Parser


DB.init()


def parse(event, context):
    parser = Parser()
    cfps = parser.get_cfps()
    CFP.create_if_needed(cfps)


def telegram_bot(event, context):
    body = event.get('body')

    if event.get('httpMethod') == 'POST' and body:
        bot.update(body)

        if bot.message_received == '/start':
            bot.send_start_message(bot.chat_id)
            logger.info(f'/start command executed by chat_id: {bot.chat_id}')

        latest_category_match = re.search(r'^(/latest) (\w+)$', bot.message_received)
        if latest_category_match:
            category = latest_category_match.groups()[-1].lower()

            cfps = CFP.get_latest_by_category(category)
            if cfps:
                for cfp in cfps:
                    message = bot.format_cfp(cfp)
                    bot.send_message(bot.chat_id, message)
                    logger.info(
                        f'/latest <category> command executed by chat_id: {bot.chat_id}'
                        f'with message: {message}'
                    )
            else:
                message = (
                    f'Sorry, I could not find any {category} CFPs 😔\n\n'
                    f'You can find all the available categories with the /categories command!'
                )
                bot.send_message(bot.chat_id, message)
                logger.info(
                    f'/latest <category> returned empty by chat_id: {bot.chat_id}'
                    f'with category: {category}'
                )

        if bot.message_received == '/latest':
            for cfp in CFP.get_latest():
                message = bot.format_cfp(cfp)
                bot.send_message(bot.chat_id, message)
                logger.info(
                    f'/latest command executed by chat_id: {bot.chat_id} with message: {message}'
                )

        if bot.message_received == '/categories':
            message = '👉  *Here are the categories available:*\n\n'
            for entry in CFP.get_categories():
                message = message + entry.category + '\n'

            bot.send_message(bot.chat_id, message)
            logger.info(
                f'/categories command executed by chat_id: {bot.chat_id} with message: {message}'
            )

        return TelegramBot.ok_response()

    return TelegramBot.error_response()


def send_telegram_messages_to_channel(event, context):
    not_sent = CFP.get_not_sent_telegram()

    for cfp in not_sent:
        message = bot.format_cfp(cfp)
        bot.send_message(TELEGRAM_CFPLAND_CHANNEL, message)
        cfp.sent_on_telegram()
        logger.info(f'sent new CFP to chat_id: {TELEGRAM_CFPLAND_CHANNEL} with message {message}')


def set_telegram_webhook(event, context):
    webhook = bot.set_webhook(event)

    if webhook:
        return TelegramBot.ok_response()

    return TelegramBot.error_response()

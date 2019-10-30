import json

import telegram

from ..constants import COULD_NOT_UPDATE_BOT_INFORMATION, TELEGRAM_TOKEN
from ..logger import logger


START_MESSAGE = """
Hello human, I'm the [CFP Land](https://www.cfpland.com/) Telegram Bot 🗣🤖

I'm mainly used as a bot in the [CFP Land Channel](https://t.me/cfpland), where I send the latest Call for Papers. Be sure to join me there!

Here, I can send you a customized list of CFPs with these commands:

- /latest: get the latest 10 CFPs.
- /latest <category>: get the latest 10 CFPs in a specific category, like DevOps.
- /thismonth: get the CFPs open for this month.
- /categories: get the CFPs categories available.

If you have any issue with me, please open an issue in my [code base repository](https://github.com/jonatasbaldin/cfpland-telegram-bot).

Made with ❤️ by [jonatasbaldin](https://twitter.com/jonatasbaldin).
"""  # noqa: E501


class TelegramBot:
    bot = None
    chat_id = None
    message_received = None

    def __init__(self):
        self.bot = telegram.Bot(TELEGRAM_TOKEN)

    def update(self, request_body):
        update = telegram.Update.de_json(json.loads(request_body), self.bot)
        try:
            self.chat_id = update.message.chat.id
            self.message_received = update.message.text
        except AttributeError as exception:
            logger.exception(
                {
                    'description': COULD_NOT_UPDATE_BOT_INFORMATION,
                    'exception': exception,
                },
                code=COULD_NOT_UPDATE_BOT_INFORMATION, exc_info=True,
            )

            return self.error_response()

    def send_message(self, chat_id, text):
        self.bot.send_message(
            chat_id=chat_id,
            text=text,
            parse_mode=telegram.ParseMode.MARKDOWN,
            disable_web_page_preview=True,
        )

    def send_start_message(self, chat_id):
        self.send_message(chat_id, START_MESSAGE)

    def format_cfp(self, item):
        return (
            f'👉  *{item.title}*\n\n'
            f'💻  *Category:* {item.category}\n'
            f'🚨  *CFPs Due:* {item.cfp_end_date}\n'
            f'💅  *Perks:* {item.perk_list}\n'
            f'🗓  *Conference Date:* {item.event_start_date}\n'
            f'🌍  *Location:* {item.location}\n'
            f'⚡️  [Click here to send your talk!]({item.link})\n\n'
            f'–––––––––––––––––––––––––––––––––––'
        )

    def set_webhook(self, url):
        return self.bot.set_webhook(url)

    def ok_response(self):
        return {
            'statusCode': 200,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps('ok')
        }

    def error_response(self, body='something went wrong'):
        return {
            'statusCode': 400,
            'body': json.dumps(body),
        }


bot = TelegramBot()

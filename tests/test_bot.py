from inspect import cleandoc

from cfpland_telegram_bot.bot.main import send_telegram_messages_to_channel
from cfpland_telegram_bot.bot.main import Cfp
from cfpland_telegram_bot.bot.bot import bot


class TestSendTelegramMessageToChannel:
    def test_send_message_successful(self, mocker, dynamodb_stream_event):
        mocker.patch('cfpland_telegram_bot.bot.bot.TelegramBot.send_message')
        send_telegram_messages_to_channel(dynamodb_stream_event, '')


class TestTelegramBot:
    def test_format_cfp_successful(self):
        cfp = Cfp(
            'title',
            'category',
            'cfp_end_date',
            'perk_list',
            'event_start_date',
            'location',
            'link',
        )

        cfp = bot.format_cfp(cfp)

        formatted_cfp = (
            """
            👉  *title*

            💻  *Category:* category
            🚨  *CFPs Due:* cfp_end_date
            💅  *Perks:* perk_list
            🗓  *Conference Date:* event_start_date
            🌍  *Location:* location
            ⚡️  [Click here to send your talk!](link)

            –––––––––––––––––––––––––––––––––––
            """
        )

        assert cfp == cleandoc(formatted_cfp)

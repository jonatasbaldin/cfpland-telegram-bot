from datetime import datetime

from peewee import *  # noqa: F403
import pw_database_url

from ..constants import (
    COULD_NOT_CREATE_CFP,
    COULD_NOT_FORMAT_DATES_CFP,
    CREATED_CFP,
    DATABASE_URL,
)
from ..logger import logger


DB_PARAMS = pw_database_url.parse(DATABASE_URL)


class DB:
    db = PostgresqlDatabase(
        DB_PARAMS.get('name'),
        user=DB_PARAMS.get('user'),
        password=DB_PARAMS.get('password'),
        host=DB_PARAMS.get('host'),
        port=DB_PARAMS.get('port')
    )

    @classmethod
    def init(cls):
        cls.db.create_tables([CFP])


class CFP(Model):
    title = CharField(unique=True, primary_key=True)
    description = CharField(max_length=1024)
    link = CharField(max_length=1024)
    category = CharField()
    event_start_date = DateField()
    cfp_end_date = DateField()
    location = CharField()
    perk_list = CharField(default="None")
    telegram_message_sent = BooleanField(default=False)

    class Meta:
        database = DB.db

    @classmethod
    def create_if_needed(cls, cfps):
        for cfp in cfps:
            title = cfp.get('title')

            try:
                date_pattern = '%Y-%m-%d'

                cfp_end_date = cfp.get('cfp_end_date')
                event_start_date = cfp.get('event_start_date')

                cfp_end_date = datetime.strptime(cfp_end_date, date_pattern).date()
                event_start_date = datetime.strptime(event_start_date, date_pattern).date()
            except ValueError as exception:
                logger.exception(
                    {
                        'description': COULD_NOT_FORMAT_DATES_CFP,
                        'cfp_title': title,
                        'exception': exception,
                    },
                    code=COULD_NOT_FORMAT_DATES_CFP, exc_info=True,
                )

            try:
                cfp, created = cls.get_or_create(title=title, defaults=cfp)
                if created:
                    logger.info({
                        'description': CREATED_CFP,
                        'cfp_title': title,
                    }, code=CREATED_CFP)
            except IntegrityError as exception:
                logger.exception(
                    {
                        'description': COULD_NOT_CREATE_CFP,
                        'cfp_title': title,
                        'exception': exception,
                    }, code=COULD_NOT_CREATE_CFP, exc_info=True,
                )

    @classmethod
    def get_latest(cls):
        today = datetime.now().date()

        return (
            cls
            .select()
            .where(cls.cfp_end_date >= today)
            .order_by(cls.cfp_end_date.desc())
            .limit(10)
        )[::-1]

    @classmethod
    def get_latest_by_category(cls, category):
        today = datetime.now().date()

        return (
            cls
            .select()
            .where(fn.Lower(cls.category) == category)
            .where(cls.cfp_end_date >= today)
            .order_by(cls.cfp_end_date.desc())
            .limit(10)
        )[::-1]

    @classmethod
    def get_categories(cls):
        return (
            cls
            .select(cls.category)
            .distinct()
        )

    @classmethod
    def get_not_sent_telegram(cls):
        return cls.select().where(cls.telegram_message_sent == False)  # noqa: E712

    def sent_on_telegram(self):
        self.telegram_message_sent = True
        self.save()

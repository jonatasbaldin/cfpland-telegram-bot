from base64 import b64decode
import gzip
import json

import boto3
from glom import glom

from ..constants import (
    COULD_NOT_CREATE_CFP,
    COULD_NOT_FORMAT_DATES_CFP,
    CREATED_CFP,
    SENT_TO_TELEGRAM_CHANNEL,
)
from ..logger import logger


cloudwatch = boto3.client('cloudwatch')


IGNORED_MESSAGE_PREFIX = ('START', 'END', 'REPORT')


def decode_log_event(event):
    data = glom(event, 'awslogs.data')
    if data:
        return json.loads(gzip.decompress(b64decode(data)).decode())


def get_log_messages(log_data):
    log_messages = []

    for event in log_data.get('logEvents'):
        message = event.get('message')

        if message.startswith(IGNORED_MESSAGE_PREFIX):
            continue

        try:
            log_messages.append(json.loads(message))
        except json.JSONDecodeError:
            logger.exception('could not decode message', message=message)

    return log_messages


def get_message_type(structured_log):
    description = glom(structured_log, 'event.description')
    if not description:
        return

    if description in [CREATED_CFP, SENT_TO_TELEGRAM_CHANNEL]:
        return description


def send_created_cfp_metric():
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Created',
                'Value': 1.0
            },
        ],
        Namespace='CFP/DATABASE',
    )


def send_could_not_create_cfp_metric():
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Failed to Create',
                'Value': 1.0
            },
        ],
        Namespace='CFP/DATABASE',
    )


def send_could_not_format_dates_cfp_metric():
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Failed to Format Dates',
                'Value': 1.0
            },
        ],
        Namespace='CFP/DATABASE',
    )


def send_sent_to_telegram_metric():
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': 'Sent',
                'Value': 1.0
            },
        ],
        Namespace='CFP/TELEGRAM',
    )


def send_metrics(event, context):
    log_data = decode_log_event(event)
    log_messages = get_log_messages(log_data)

    for message in log_messages:
        message_type = get_message_type(message)

        if message_type == CREATED_CFP:
            send_created_cfp_metric()

        if message_type == SENT_TO_TELEGRAM_CHANNEL:
            send_sent_to_telegram_metric()

        if message_type == COULD_NOT_CREATE_CFP:
            send_could_not_create_cfp_metric()

        if message_type == COULD_NOT_FORMAT_DATES_CFP:
            send_could_not_format_dates_cfp_metric()
import os

import boto3
from moto import mock_dynamodb2
import pytest

from cfpland_telegram_bot.constants import DYNAMODB_TABLE


@pytest.fixture(scope='function')
def aws_credentials():
    """
    Making sure we don't use any valid AWS account, if the mock fails.
    """
    os.environ['AWS_ACCESS_KEY_ID'] = 'testing'
    os.environ['AWS_SECRET_ACCESS_KEY'] = 'testing'
    os.environ['AWS_SECURITY_TOKEN'] = 'testing'
    os.environ['AWS_SESSION_TOKEN'] = 'testing'


@pytest.fixture(scope='function')
def dynamodb_table(aws_credentials):
    with mock_dynamodb2():
        dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
        table = dynamodb.create_table(
            TableName=DYNAMODB_TABLE,
            AttributeDefinitions=[
                {
                    'AttributeName': 'cfpEndDate',
                    'AttributeType': 'S',
                },
                {
                    'AttributeName': 'category',
                    'AttributeType': 'S',
                },
            ],
            KeySchema=[
                {
                    'AttributeName': 'category',
                    'KeyType': 'HASH',
                },
                {
                    'AttributeName': 'cfpEndDate',
                    'KeyType': 'RANGE',
                }
            ]
        )

        yield table


@pytest.fixture()
def dynamodb_stream_event():
    yield {
        'Records': [
            {
                'eventID': '75a223bcaa6a59998df65e65dbdfcae8',
                'eventName': 'INSERT',
                'eventVersion': '1.1',
                'eventSource': 'aws:dynamodb',
                'awsRegion': 'eu-west-1',
                'dynamodb': {
                    'ApproximateCreationDateTime': 1565107189.0,
                    'NewImage':
                        {
                            'id': {'S': '1'},
                            'title': {'S': 'Title'},
                            'category': {'S': 'Category'},
                            'cfpEndDate': {'S': '2019-01-01'},
                            'perkList': {'S': 'None'},
                            'eventStartDate': {'S': '2019-01-01'},
                            'location': {'S': 'Remote'},
                            'link': {'S': 'https://deployeveryday.com'},
                        },
                    'SequenceNumber': '108124000000000048251595977',
                    'SizeBytes': 86,
                    'StreamViewType': 'NEW_AND_OLD_IMAGES',
                },
            }
        ]
    }

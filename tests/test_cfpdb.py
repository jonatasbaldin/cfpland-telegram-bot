from boto3.dynamodb.conditions import Key
import pytest

from cfpland_telegram_bot.exceptions import MissingCFPAttributes
from cfpland_telegram_bot.models import CFPDB


class TestCFPDB:
    def test_create_successful(self, dynamodb_table):
        cfpdb = CFPDB(dynamodb_table)

        cfp = {
            'title': 'ScotlandPHP',
            'description': 'A PHP Conference',
            'link': 'https://cfs.scotlandphp.co.uk',
            'category': 'PHP',
            'event_start_date': '2019-11-08',
            'cfp_end_date': '2019-04-22',
            'location': 'Edinburgh, U.K.',
            'perk_list': 'Travel, Hotel',
        }
        cfpdb.create(cfp)

        item = dynamodb_table.query(
            KeyConditionExpression=Key('category').eq('PHP')
        ).get('Items')[0]

        assert item.get('title') == cfp.get('title')
        assert item.get('description') == cfp.get('description')
        assert item.get('link') == cfp.get('link')
        assert item.get('category') == cfp.get('category')
        assert item.get('event_start_date') == cfp.get('eventStartDate')
        assert item.get('cfp_end_date') == cfp.get('cfpEndDate')
        assert item.get('location') == cfp.get('location')
        assert item.get('perk_list') == cfp.get('perkList')
        assert item.get('id')
        assert item.get('createdAt')

        assert dynamodb_table.item_count == 1

    def test_create_empty_cfp(self, dynamodb_table):
        cfpdb = CFPDB(dynamodb_table)

        cfp = {}

        with pytest.raises(MissingCFPAttributes):
            assert cfpdb.create(cfp)

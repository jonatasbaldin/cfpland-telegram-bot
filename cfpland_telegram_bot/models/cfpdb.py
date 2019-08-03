from uuid import uuid4

from botocore.exceptions import ClientError

from ..constants import (
    COULD_NOT_CREATE_CFP,
    CREATED_CFP_DYNAMODB,
)
from ..exceptions import MissingCFPAttributes
from ..logger import logger


class CFPDB:
    def __init__(self, dynamodb_table):
        self.dynamodb_table = dynamodb_table

    def create(self, cfp):
        title = cfp.get('title')
        category = cfp.get('category')
        cfp_end_date = cfp.get('cfp_end_date')
        event_start_date = cfp.get('event_start_date')
        link = cfp.get('link', 'None')
        description = cfp.get('description', 'None')
        location = cfp.get('location', 'None')
        perk_list = cfp.get('perk_list', 'None')

        if None in [title, category, cfp_end_date, event_start_date]:
            raise MissingCFPAttributes(cfp)

        try:
            self.dynamodb_table.put_item(
                Item={
                    'id': str(uuid4()),
                    'cfpEndDate': cfp_end_date,
                    'title': title,
                    'description': description,
                    'link': link,
                    'category': category,
                    'eventStartDate': event_start_date,
                    'location': location,
                    'perkList': perk_list,
                }
            )

            logger.info({
                'description': CREATED_CFP_DYNAMODB,
                'cfp': cfp,
            }, code=CREATED_CFP_DYNAMODB)
        except ClientError as exception:
            logger.exception(
                {
                    'description': COULD_NOT_CREATE_CFP,
                    'cfp': cfp,
                    'exception': exception,
                }, code=COULD_NOT_CREATE_CFP, exc_info=True,
            )

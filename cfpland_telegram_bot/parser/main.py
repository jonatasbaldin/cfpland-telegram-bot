import boto3

from ..constants import DYNAMODB_TABLE
from .parser import Parser
from ..models import CFP, CFPDB, DB


DB.init()
table = boto3.resource('dynamodb').Table(DYNAMODB_TABLE)
cfpdb = CFPDB(table)


def parse(event, context):
    parser = Parser()
    cfps = parser.get_cfps()
    CFP.create_if_needed(cfps)

    for cfp in cfps:
        cfpdb.create(cfp)

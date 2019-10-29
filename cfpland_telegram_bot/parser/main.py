import boto3

from .parser import Parser
from ..models import CFP, CFPDB, DB


DB.init()


def parse(event, context):
    parser = Parser()
    cfps = parser.get_cfps()
    CFP.create_if_needed(cfps)

    for cfp in cfps:
        cfpdb.create(cfp)

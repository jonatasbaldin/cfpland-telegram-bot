from .parser import Parser
from ..models import CFP, DB


DB.init()


def parse(event, context):
    parser = Parser()
    cfps = parser.get_cfps()
    CFP.create_if_needed(cfps)

from .parser import Parser
from ..iopipe import iopipe
from ..models import CFP, DB


DB.init()


@iopipe
def parse(event, context):
    parser = Parser()
    cfps = parser.get_cfps()
    CFP.create_if_needed(cfps)

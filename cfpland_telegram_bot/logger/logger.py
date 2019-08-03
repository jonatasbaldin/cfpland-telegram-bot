import structlog

from ..constants import ENVIRONMENT


structlog_processors = [
    structlog.stdlib.add_log_level,
    structlog.stdlib.PositionalArgumentsFormatter(),
    structlog.processors.StackInfoRenderer(),
    structlog.processors.format_exc_info,
    structlog.processors.TimeStamper(fmt='iso', utc=True),
    structlog.processors.UnicodeDecoder(),
]

if ENVIRONMENT in ['prod', 'test']:
    structlog_processors.append(structlog.processors.JSONRenderer())
else:
    structlog_processors.append(structlog.dev.ConsoleRenderer())


structlog.configure_once(
    processors=structlog_processors,
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

import logging

# Set up the logging configuration
logging.basicConfig(
    filename='etc/log/debug.log',
    encoding="utf-8",        # I'm getting a warning message? LSP problem?
    filemode="a",            # a is default
    level=logging.DEBUG,
    format="{levelname} : {message} | {module}:{lineno} | {asctime}",
    style="{",
    datefmt="%Y-%m-%d %H:%M",
)

# init the logger variable
logger = logging.getLogger(__name__)

# First logger print
logger.info('======== logger started ========')

# It seems that the variable 'logger' needs to be specifically imported to work;
